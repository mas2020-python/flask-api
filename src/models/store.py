from internal.db import db

"""
Item model is the representation of the DB object item
"""


class StoreModel(db.Model):
    # -- start SQLAlchemy info
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    """relationship with item model (see the other class). lazy defines when SQLAlchemy will load the data from the 
    database: 
    * 'select': (default: true) means that SQLAlchemy will load the data as necessary in one go using a 
    standard select statement. 
    * 'joined': tells SQLAlchemy to load the relationship in the same query as the parent 
    using a JOIN statement. 
    * 'subquery': works like 'joined' but instead SQLAlchemy will use a subquery. 
    * 'dynamic': is special and can be useful if you have many items and always want to apply additional SQL filters to 
    them. Instead of loading the items SQLAlchemy will return another query object which you can further refine before 
    loading the items. Note that this cannot be turned into a different loading strategy when querying so it’s often 
    a good idea to avoid using this in favor of lazy=True. A query object equivalent to a dynamic user.addresses 
    relationship can be created using Address.query.with_parent(user) while still being able to use lazy or eager 
    loading on the relationship itself as necessary. 
    
    It is also possible to add a back ref on the child object, in this case ItemModel, to see the store object
    associated with the child using:
    items = db.relationship('ItemModel', lazy='dynamic', backref=db.backref('store', lazy='joined'))
    at this point in the ItemModel is possible to reference the self.store property (without ever having created it)
    """
    # one to many relationship from store -> items
    items = db.relationship('ItemModel', lazy='dynamic')
    # -- end SQLAlchemy info

    def __init__(self, name):
        self.name = name

    # JSON representation of an Item
    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'items': [item.json() for item in self.items.all()]
        }

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
