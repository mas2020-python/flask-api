from flask_restful import Api

from resources.test import Test
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import User, UserList, UserLogin, TokenRefresh


def add_resources(api: Api):
    # Add resources and binding with the HTTP URL
    api.add_resource(Test, '/test')
    api.add_resource(Item, '/items/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(Store, '/stores/<int:_id>')
    api.add_resource(StoreList, '/stores')
    api.add_resource(User, '/users/<int:user_id>')
    api.add_resource(UserList, '/users')
    api.add_resource(UserLogin, '/login')
    api.add_resource(TokenRefresh, '/refresh')
