# temporary in memory db for test
items = []


class User():
    def __init__(self, username, _id, password):
        self.username = username
        self.id = _id
        self.password = password


users = [
    User("ag", 'admin', "test")
]

# Dictionaries creation (u.username is the key, u is the value)
username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}
