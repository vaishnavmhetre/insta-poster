from peewee import *

from DB.Models import User as DBUser

def getRandomUser():
    try:
        user = DBUser.select().order_by(fn.Random()).where(DBUser.exhausted == False).limit(1).get()
        return user
    except DBUser.DoesNotExist as e:
        return None
