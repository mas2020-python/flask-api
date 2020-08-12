import os
import sys
from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from resources.test import Test
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import User, UserList, UserLogin, TokenRefresh
from flask_jwt_extended import JWTManager
from internal.db import db
from utils.config import API_SRV
import toml
import logging
import logging.config

from flask.logging import default_handler

"""
Using flask_restful jsonify for object that are not dictionary is not needed cause flask restful
do it for us.
"""
logger: logging.Logger
# Flask api global variable
api: Api
app: Flask


def read_api_config():
    try:
        API_SRV.config = toml.load('config/api-server.toml')
    except Exception as e:
        print("Houston, we have a problem: ", e.__str__())
        sys.exit(1)


# Set the logger
def set_logger():
    global logger
    try:
        # Does log file exist?
        if not os.path.isfile(API_SRV.config['log']['conf_file']):
            raise Exception("log config file ({}) not found!".format(API_SRV.config['log']['conf_file']))
        logging.config.fileConfig(fname=API_SRV.config['log']['conf_file'], disable_existing_loggers=True)
        # Get the logger specified in the file
        logger = logging.getLogger(API_SRV.config['log']['default_logger'])
    except Exception as e:
        print("Houston, we have a problem: ", e.__str__())
        sys.exit(1)


def create_app():
    global api, app
    # creating main app
    app = Flask(__name__)
    app.secret_key = "secret-key"  # or config as app.config['JWT_SECRET_KEY']
    # in order to use only the SQLAlchemy modification tracker and not the FlaskSQLAlchemy one
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = API_SRV.config['server']['db_connection']
    app.config['PROPAGATE_EXCEPTIONS'] = True
    api = Api(app)

    # using a decorator of Flask to execute the following method before the first request comes to Flask
    @app.before_first_request
    def create_table():
        db.create_all()

    # jtw extended token settings
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = API_SRV.config['security']['token_expiration']
    jwt = JWTManager(app)

    @jwt.user_claims_loader
    def add_claims_to_jwt(identity):
        """
        This method is used to add some claims to the payload of the JWT token as well. The claims are added
        in the form of a dictionary (json object) as:
        "user_claims": {
            "is_admin": true
        }
        :param identity: identity set in UserLogin post method
        :return:
        """
        # suppose for test that if a user has id == 1 is admin. We set identity to the user_id
        is_admin = True if identity == 1 else False
        return {'is_admin': is_admin}

    @jwt.expired_token_loader
    def expired_token_callback():
        return jsonify({
            'description': 'The token has expired',
            'error': 'token_expired'
        }), 401

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


def main():
    try:
        # read config and load logger
        read_api_config()
        set_logger()
        create_app()
        add_resources(api)
        # connect the SQLAlchemy object to the app
        db.init_app(app)
        # run the test server, Debug=True helps to debug in case of any error
        api_env = os.environ[API_SRV.config['server']['api_env']]
        logger.debug(f"set token expiration to {API_SRV.config['security']['token_expiration']} seconds")
        if api_env == 'test':
            logger.info(f"Application is starting in TEST environment (version: {API_SRV.config['server']['version']})")
            app.run(host=API_SRV.config['server']['address'], port=API_SRV.config['server']['port'],
                    debug=True if API_SRV.config['server']['debug'] else False)
        else:
            logger.info(f"Application is starting in PRODUCTION env (version: {API_SRV.config['server']['version']})")
    except KeyError as e:
        logger.error(f"Houston, we have a problem finding the env variable: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Houston, we have a problem: {str(e)}")
        sys.exit(1)


# start point for the Application
main()
