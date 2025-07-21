import flask
from sqlalchemy.sql import func

import models
import forms


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "This is secret key"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://coe:CoEpasswd@localhost:5432/coedb"

models.init_app(app)


@app.route("/")
def index():
    db = models.db
    notes = db.session.execute(
        db.select(models.Note).order_by(models.Note.title)
    ).scalars()
    return flask.render_template(
        "index.html",
        notes=notes,
    )


@app.route("/notes/create", methods=["GET", "POST"])
def notes_create():
    form = forms.NoteForm()
    if not form.validate_on_submit():
        if flask.request.method == "POST":
            print("error", form.errors)
        return flask.render_template(
            "notes-create.html",
            form=form,
        )
    
    note = models.Note()
    # กำหนดค่าฟิลด์ด้วยตัวเองแทนการใช้ populate_obj
    note.title = form.title.data
    note.description = form.description.data
    note.tags = []  # เริ่มต้นด้วย list ว่าง

    db = models.db
    for tag_name in form.tags.data:
        if tag_name:  # ตรวจสอบว่าไม่เป็นสตริงว่าง
            # หา tag ที่มีอยู่แล้ว
            tag = (
                db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
                .scalars()
                .first()
            )

            # ถ้าไม่มี tag นี้ ให้สร้างใหม่
            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)

            # เพิ่ม Tag object เข้าไปในความสัมพันธ์
            note.tags.append(tag)

    db.session.add(note)
    db.session.commit()

    return flask.redirect(flask.url_for("index"))


@app.route("/notes/edit/<int:note_id>", methods=["GET", "POST"])
def notes_edit(note_id):
    db = models.db
    note = db.session.get(models.Note, note_id)
    if not note:
        flask.abort(404)

    form = forms.NoteForm(obj=note)
    
    # กรณีเป็น GET request ให้แสดงข้อมูล tags ปัจจุบัน
    if flask.request.method == "GET":
        form.tags.data = [tag.name for tag in note.tags]
    
    if flask.request.method == "POST":
        if not form.validate_on_submit():
            print("error", form.errors)
            return flask.render_template(
                "notes-edit.html",
                form=form,
                note_id=note_id,
            )
        
        # อัพเดตเฉพาะ title และ description
        note.title = form.title.data
        note.description = form.description.data
        note.tags = []
        note.updated_date = func.now()

        for tag_name in form.tags.data:
            if tag_name:  # ตรวจสอบว่าไม่เป็นสตริงว่าง
                tag = (
                    db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
                    .scalars()
                    .first()
                )
                if not tag:
                    tag = models.Tag(name=tag_name)
                    db.session.add(tag)
                note.tags.append(tag)

        db.session.commit()
        return flask.redirect(flask.url_for("index"))

    return flask.render_template("notes-edit.html", form=form, note_id=note_id)


@app.route("/notes/delete/<int:note_id>", methods=["POST"])
def notes_delete(note_id):
    db = models.db
    note = db.session.get(models.Note, note_id)
    if not note:
        flask.abort(404)
    
    db.session.delete(note)
    db.session.commit()
    return flask.redirect(flask.url_for("index"))


@app.route("/tags/<tag_name>")
def tags_view(tag_name):
    db = models.db
    tag = (
        db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
        .scalars()
        .first()
    )
    
    if not tag:
        flask.abort(404)
    
    notes = db.session.execute(
        db.select(models.Note).where(models.Note.tags.any(id=tag.id)).order_by(models.Note.title)
    ).scalars()

    return flask.render_template(
        "tags-view.html",
        tag_name=tag_name,
        notes=notes,
    )


if __name__ == "__main__":
    app.run(debug=True)