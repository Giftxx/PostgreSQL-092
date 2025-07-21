from flask import Flask
from typing import List
from flask_sqlalchemy import SQLAlchemy

import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_app(app):
    db.init_app(app)

    with app.app_context():
        db.create_all()


note_tag_m2m = db.Table(
    "note_tag",
    sa.Column("note_id", sa.ForeignKey("notes.id"), primary_key=True),
    sa.Column("tag_id", sa.ForeignKey("tags.id"), primary_key=True),
)


class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String, nullable=False, unique=True)
    
    # เพิ่ม relationship เพื่อให้เข้าถึง notes จาก tag ได้
    notes: Mapped[List["Note"]] = relationship(secondary=note_tag_m2m, back_populates="tags")

    created_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Tag {self.name}>'


class Note(db.Model):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    description: Mapped[str] = mapped_column(sa.Text)

    tags: Mapped[List[Tag]] = relationship(secondary=note_tag_m2m, back_populates="notes")

    created_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now())
    updated_date = mapped_column(sa.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f'<Note {self.title}>'