import sqlite3

# temporary in memory db for test
items = []

# If started as main module create temp data.db and insert users inside
if __name__ == "__main__":
    # connection to temp db
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    # create a tuple for the user
    user = (11, "ag", "test")
    # insert row (to add more rows use executemany
    cursor.execute("INSERT INTO users VALUES (?,?,?)", user)
    # commit the changes
    connection.commit()
    cursor.execute("INSERT INTO items VALUES (1,'test',10.99,1)")
    cursor.execute("INSERT INTO items VALUES (2,'test2',12.99,1)")
    cursor.execute("INSERT INTO items VALUES (3,'test3',99.99,1)")
    # commit the changes
    connection.commit()

    connection.close()
