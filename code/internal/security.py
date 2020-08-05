"""
This file is for managing security in combination with the JWT technique.
We have to mandatory methods:
- authenticate: use for authentication of the users
- identity: use to get the payload
"""
from models.user import UserModel
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload['identity']
    # return the object to save in current_identity variable
    return UserModel.find_by_id(user_id)
