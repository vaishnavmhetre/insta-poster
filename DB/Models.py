from peewee import *

from DB.DBInit import DBInit


class BaseModel(Model):
    class Meta:
        database = DBInit("./storage/my_db.sqlite").db


class User(BaseModel):
    pk = BigIntegerField()
    username = CharField()
    exhausted = BooleanField(default=False)


class Post(BaseModel):
    pk = BigIntegerField()
    user = ForeignKeyField(User, backref="posts")
