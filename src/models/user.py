import sqlite3
from internal.db import db


class UserModel(db.Model):
    # -- start SQLAlchemy info
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    # -- end SQLAlchemy info

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # JSON representation of the User
    def json(self):
        return {
            'id': self.id,
            'username': self.username,
        }

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
