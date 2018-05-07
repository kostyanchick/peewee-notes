from flask import Markup
from markdown import markdown
from micawber import parse_html
from peewee import *
from datetime import datetime

from app import pg_db, oembed


class BaseModel(Model):
    class Meta:
        database = pg_db

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()
    email = CharField(unique=True)
    join_date = DateTimeField()
    about_me = TextField(null=True)
    last_seen = DateTimeField(null=True)
    photo_file_name = CharField(default='default.png')

class Note(BaseModel):
    user = ForeignKeyField(User, backref='notes')
    content = TextField()
    timestamp = DateTimeField(default=datetime.now())
    archived = BooleanField(default=False)

    def html(self):
        html = parse_html(
            markdown(self.content),
            oembed,
            maxwidth=300,
            urlize_all=True)
        return Markup(html)

    @classmethod
    def user_notes(cls, user):
        return (Note.select()
                .where(Note.user == user, Note.archived == False)
                .order_by(Note.timestamp.desc()))