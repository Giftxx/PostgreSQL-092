from wtforms_sqlalchemy.orm import model_form
from flask_wtf import FlaskForm
from wtforms import Field, widgets

import models


class TagListField(Field):
    widget = widgets.TextInput()

    def __init__(self, label="", validators=None, remove_duplicates=True, **kwargs):
        super().__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates
        self.data = []

    def process_formdata(self, valuelist):
        data = []
        if valuelist:
            data = [x.strip() for x in valuelist[0].split(",")]

        if not self.remove_duplicates:
            self.data = data
            return

        self.data = []
        for d in data:
            if d and d not in self.data:  # เช็คให้แน่ใจว่าไม่เป็นสตริงว่าง
                self.data.append(d)

    def _value(self):
        if self.data:
            return ", ".join(self.data)
        else:
            return ""


BaseNoteForm = model_form(
    models.Note, 
    base_class=FlaskForm, 
    exclude=["created_date", "updated_date"], 
    db_session=models.db.session
)


class NoteForm(BaseNoteForm):
    tags = TagListField("Tags")