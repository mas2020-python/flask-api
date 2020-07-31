import sqlite3
from internal.db import db

"""
Item model is the representation of the DB object item
"""
class ItemModel(db.Model):
    # -- start SQLAlchemy info
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float(precision=2))
    # connection with the store table: the db.ForeignKey connects the stores id field with the store_id field. It is
    # a classic way as a Foreign key create a link between two tables
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')
    # -- end SQLAlchemy info

    def __init__(self, name, price, store_id):
        #self.id = ItemModel.id
        self.name = name
        self.price = price
        self.store_id = store_id


    # JSON representation of an Item
    def json(self):
        return {'id': self.id, 'name': self.name, 'price': self.price}

    @classmethod
    # Search an item by name
    def find_by_name(cls, name):
        # return the first row matching with the filter using FlaskSQLAlchemy
        return cls.query.filter_by(name=name).first()

    """
    Save and update at the same time
    """
    def insert(self):
        db.session.add(self)
        db.session.commit()
        """ save into db (before SQLAlchemy)
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()
        """

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

""" with SQLAlchemy no longer needed
    def update(self):
        # save into db
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()
"""