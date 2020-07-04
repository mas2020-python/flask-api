"""
This file is for managing security in combination with the JWT technique.
We have to mandatory methods:
- authenticate: use for authentication of the users
- identity: use to get the payload
"""
import tmpdb


def authenticate(username, password):
    user = tmpdb.User.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return tmpdb.User.find_by_id(user_id)
