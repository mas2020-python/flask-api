import os
import sys
from datetime import timedelta
from flask import Flask
from flask_restful import Api
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from flask_jwt import JWT
from internal.security import authenticate, identity
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
    app.secret_key = "secret-key"
    # in order to use only the SQLAlchemy modification tracker and not the FlaskSQLAlchemy one
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = API_SRV.config['server']['db_connection']
    api = Api(app)

    # using a decorator of Flask to execute the following method before the first request comes to Flask
    @app.before_first_request
    def create_table():
        db.create_all()

    # jtw token (create /auth route: pass a JWT + token as Authorization Header)
    """ if you need:
    - to change /auth URL in /login use:
    app.config['JWT_AUTH_URL_RULE'] = '/login'
    - to change token expiration time use (example set half an hour):
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
    """
    app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
    jwt = JWT(app, authenticate, identity)


def add_resources(api: Api):
    # Add resources and binding with the HTTP URL
    api.add_resource(Item, '/items/<string:name>')
    api.add_resource(ItemList, '/items')
    api.add_resource(Store, '/stores/<int:_id>')
    api.add_resource(StoreList, '/stores')


def main():
    try:
        # read config and load logger
        read_api_config()
        create_app()
        set_logger()
        # log = logging.getLogger('werkzeug')
        # log.disabled = True
        # print(logger.handlers)
        add_resources(api)
        # connect the SQLAlchemy object to the app
        db.init_app(app)
        # run the test server, Debug=True helps to debug in case of any error
        api_env = os.environ[API_SRV.config['server']['api_env']]
        if api_env == 'test':
            logger.info(f"Application is starting in TEST environment (version: {API_SRV.config['server']['version']})")
            app.run(port=API_SRV.config['server']['port'], debug=True if API_SRV.config['server']['debug'] else False)
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
