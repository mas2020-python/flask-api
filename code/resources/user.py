from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity
)
from models.user import UserModel
import logging
from utils.config import API_SRV

"""
Resources to manage users.
"""
# Parse the args in the JSON payload to get all the arguments you specified here.
_user_parser = reqparse.RequestParser()

_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be empty!")

_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be empty!")


class User(Resource):
    # Parse the args in the JSON payload to get all the arguments you specified here.
    parser = reqparse.RequestParser()

    # parser.add_argument('price',
    #                     type=float,
    #                     required=True,
    #                     help="This field cannot be empty!")

    def __init__(self):
        # Get the logger specified in the file
        self.logger = logging.getLogger(API_SRV.config['log']['default_logger'])

    # @jwt_required()
    def get(self, user_id):
        user: UserModel = UserModel.find_by_id(user_id)
        if user:
            return user.json(), 200
        return {'message': 'User not found'}, 404

    # Delete a single element
    def delete(self, user_id):
        user: UserModel = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
            return 204
        return {'message': 'User not found'}, 404


class UserList(Resource):
    def __init__(self):
        # Get the logger specified in the file
        self.logger = logging.getLogger(API_SRV.config['log']['default_logger'])

    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}, 200

    def post(self):
        # if OK, parse args
        data = _user_parser.parse_args()
        # username must be unique
        if UserModel.find_by_username(data['username']):
            return {'message': 'username is already present on the system'}, 400

        # save into db
        try:
            user = UserModel(**data)
            user.insert()
        except Exception as e:
            self.logger.error(str(e))
            return {'message': f"An error occurred during saving an item, read log for major details"}, 500

        # return item with the 201 http code
        return user.json(), 201


class UserLogin(Resource):
    """
    Class that verifies login credentials and create jwt token.
    """

    def __init__(self):
        # Get the logger specified in the file
        self.logger = logging.getLogger(API_SRV.config['log']['default_logger'])

    def post(self):
        # get data from parser
        data = _user_parser.parse_args()

        # find user and check password
        user: UserModel = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200
        return {'message': 'Invalid credentials'}, 401

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        # we get the current user from the token
        current_user = get_jwt_identity()
        # we generate a new token based on this identity and not refreshable
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
