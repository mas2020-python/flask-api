"""
This file is for managing security in combination with the JWT technique.
We have to mandatory methods:
- authenticate: use for authentication of the users
- identity: use to get the payload
"""
import tmpdb


def authenticate(username, password):
    user = tmpdb.username_mapping.get(username, None)
    if user and user.password == password:
        return user


def identity(payload):
    user_id = payload['identity']
    return tmpdb.userid_mapping.get(user_id, None)
