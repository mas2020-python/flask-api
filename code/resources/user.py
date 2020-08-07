from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel
import logging
from utils.config import API_SRV

"""
Resource to manage users.
"""


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
    # Parse the args in the JSON payload to get all the arguments you specified here.
    parser = reqparse.RequestParser()

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be empty!")

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be empty!")

    def __init__(self):
        # Get the logger specified in the file
        self.logger = logging.getLogger(API_SRV.config['log']['default_logger'])

    def get(self):
        return {'users': [user.json() for user in UserModel.find_all()]}, 200

    def post(self):
        # if OK, parse args
        data = UserList.parser.parse_args()
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
