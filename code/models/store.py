from internal.db import db

"""
Item model is the representation of the DB object item
"""
class StoreModel(db.Model):
    # -- start SQLAlchemy info
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # relationship with item model (see the other class). Lazy dynamic means not to load all the items related to the
    # store every time a new store model is created. This operation is demand to the query on items (adding .all to
    # self.items in json method)
    items = db.relationship('ItemModel', lazy='dynamic')
    # -- end SQLAlchemy info

    def __init__(self, name):
        self.name = name

    # JSON representation of an Item
    def json(self):
        return {'id': self.id, 'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    # Search an item by name
    def find_by_name(cls, name):
        # return the first row matching with the filter using FlaskSQLAlchemy
        return cls.query.filter_by(name=name).first()

    @classmethod
    # Search an item by name
    def find_by_id(cls, id):
        # return the first row matching with the filter using FlaskSQLAlchemy
        return cls.query.filter_by(id=id).first()

    """
    Save and update at the same time
    """
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
