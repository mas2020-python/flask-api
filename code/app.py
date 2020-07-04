from flask import Flask
from flask_restful import Resource, Api
from resources.item import Item
from resources.item_list import ItemList
from flask_jwt import JWT
from internal.security import authenticate, identity

"""
Using flask_restful jsonify for object that are not dictionary is not needed cause flask restful
do it for us.
"""

# creating main app
app = Flask(__name__)
app.secret_key = "secret-key"
api = Api(app)

# jtw token (create /auth route: pass a JWT + token as Authorization Header)
jwt = JWT(app, authenticate, identity)

# Add resources and binding with the HTTP URL
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

# run the test server, Debug=True helps to debug in case of any error
app.run(port=5000, debug=True)



