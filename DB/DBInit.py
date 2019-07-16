from peewee import SqliteDatabase


class DBInit:
    db = None

    def __init__(self, dbpath):
        self.db = SqliteDatabase(dbpath)
