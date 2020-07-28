import sys
from datetime import timedelta
from flask import Flask
from flask_restful import Api
from resources.item import Item
from resources.item_list import ItemList
from flask_jwt import JWT
from internal.security import authenticate, identity
from internal.db import db
from utils.config import API_SRV
import toml

"""
Using flask_restful jsonify for object that are not dictionary is not needed cause flask restful
do it for us.
"""

def read_api_config():
    try:
        API_SRV.config = toml.load('config/api-server.toml')
    except Exception as e:
        print("Houston, we have a problem: ", e.__str__())
        sys.exit(1)

def create_app() -> (Flask, Api):
    # creating main app
    app = Flask(__name__)
    app.secret_key = "secret-key"
    # in order to use only the SQLAlchemy modification tracker and not the FlaskSQLAlchemy one
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    api = Api(app)

    # jtw token (create /auth route: pass a JWT + token as Authorization Header)
    """ if you need:
    - to change /auth URL in /login use:
    app.config['JWT_AUTH_URL_RULE'] = '/login'
    - to change token expiration time use (example set half an hour):
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
    """
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
    jwt = JWT(app, authenticate, identity)

    return app, api


def add_resources(api: Api):
    # Add resources and binding with the HTTP URL
    api.add_resource(Item, '/item/<string:name>')
    api.add_resource(ItemList, '/items')


# start point for the Application
if __name__ == "__main__":
    # read config
    read_api_config()
    app, api = create_app()
    add_resources(api)
    # connect the SQLAlchemy object to the app
    db.init_app(app)
    # run the test server, Debug=True helps to debug in case of any error
    app.run(port=API_SRV.config['server']['port'], debug=True)
