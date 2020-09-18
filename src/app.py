import os
import sys
import toml
import logging
import logging.config
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from internal.db import db, sql_debug
from utils.config import API_SRV
from internal.resources import add_resources

"""
Using flask_restful jsonify for object that are not dictionary is
not needed cause flask restful do it for us.
"""
logger: logging.Logger
# Flask api global variable
api: Api
app = Flask('flask-api')


def read_api_config():
    try:
        api_server_toml = os.path.join(os.path.dirname(__file__), 'config', 'api-server.toml')
        API_SRV.config = toml.load(api_server_toml)
    except Exception as e:
        print("Houston, we have a problem in read_api_config: ", e.__str__())
        sys.exit(1)


def set_logger():
    """
    Set the logger to the folder <project>/log.
    """
    global logger
    try:
        # if the folder doesn't exist will be created
        log_folder = os.path.join(os.path.dirname(__file__), '..', 'log')
        if not os.path.isdir(log_folder):
            os.mkdir(log_folder)
        # Get the logger specified in the file
        logger = logging.getLogger(API_SRV.config['log']['default_logger'])
        logger.setLevel(API_SRV.config['log']['level'])
        # create file handler and set level to debug
        fh = logging.FileHandler(os.path.join(os.path.dirname(__file__), '..', 'log', 'app.log'))
        fh.setLevel(API_SRV.config['log']['level'])
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s - %(message)s')
        fh.setFormatter(formatter)

        # add the handlers to the logger
        logger.addHandler(fh)
    except KeyError as e:
        logger.error(f"Houston, we have a problem finding the env variable in set_logger: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print("Houston, we have a problem in set_logger: ", e)
        sys.exit(1)


def create_app():
    global api, app
    # creating main app
    app.secret_key = "secret-key"  # or config as app.config['JWT_SECRET_KEY']
    # in order to use only the SQLAlchemy modification tracker and not the FlaskSQLAlchemy one
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DB_CONNECTION']
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['DEBUG'] = API_SRV.config['server']['debug']
    api = Api(app)

    if API_SRV.config['server']['sql_debug']:
        app.after_request(sql_debug)

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


def start():
    # read config and load logger
    read_api_config()
    set_logger()
    create_app()
    add_resources(api)
    # connect the SQLAlchemy object to the app
    db.init_app(app)


def main():
    """
    Main function to start the application
    """
    try:
        start()
        if __name__ == '__main__':
            logger.info(f"Application starting in TEST environment (version: {API_SRV.config['server']['version']})")
            # run with the Flask web server for testing
            app.run(host=API_SRV.config['server']['address'], port=API_SRV.config['server']['port'])
        else:
            logger.info(f"Application starting in PRODUCTION env (version: {API_SRV.config['server']['version']})")
    except KeyError as e:
        logger.error(f"Houston, we have a problem finding the env variable: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Houston, we have a problem: {str(e)}")
        sys.exit(1)


# start point for the Application
main()
