import sqlite3

# temporary in memory db for test
items = []

"""
User class to find a user by name or id searching on sqllite 'data.db'.
"""


class User():
    def __init__(self, _id, username, password):
        self.username = username
        self.id = _id
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        # connection to temp db
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        # get the first row from a result set
        row = result.fetchone()
        if row:
            user = cls(*row)
            # classic way
            # user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        # connection to temp db
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        # get the first row from a result set
        row = result.fetchone()
        if row:
            user = cls(*row)
            # classic way
            # user = cls(row[0], row[1], row[2])
        else:
            user = None

        connection.close()
        return user


# If started as main module create temp data.db and insert users inside
if __name__ == "__main__":
    # connection to temp db
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    # create the users' table
    try:
        cursor.execute("CREATE TABLE users (id int, username text, password text)")
    except sqlite3.OperationalError:
        pass

    # create a tuple for the user
    user = (1, "ag", "test")
    # insert row (to add more rows use executemany
    cursor.execute("INSERT INTO users VALUES (?,?,?)", user)
    # commit the changes
    connection.commit()
    # connection.close()
