import sqlite3
from internal.db import db


class UserModel(db.Model):
    # -- start SQLAlchemy info
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    # -- end SQLAlchemy info

    def __init__(self, _id, username, password):
        self.username = username
        self.id = _id
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        # connection to temp db
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        # get the first row from a result set
        row = result.fetchone()
        if row:
            user = cls(*row)
            # classic way
            # user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        # connection to temp db
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        # get the first row from a result set
        row = result.fetchone()
        if row:
            user = cls(*row)
            # classic way
            # user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user
