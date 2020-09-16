import sqlite3


def create_db(db: str):
  # connection to temp db
  connection = sqlite3.connect(db)
  cursor = connection.cursor()

  # create the users' table
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER NOT NULL, 
    username VARCHAR(100), 
    password VARCHAR(100), 
    PRIMARY KEY (id)
  )
  """)

  cursor.execute("""
  CREATE TABLE IF NOT EXISTS items (
    id INTEGER NOT NULL, 
    name VARCHAR(100), 
    price FLOAT, 
    store_id INTEGER, 
    PRIMARY KEY (id), 
    FOREIGN KEY(store_id) REFERENCES stores (id))
  """)

  cursor.execute("""
  CREATE TABLE IF NOT EXISTS stores (
    id INTEGER NOT NULL, 
    name VARCHAR(80), 
    PRIMARY KEY (id))
  """)

  # create a tuple for users
  users = [(1, "ag", "test")]

  cursor.execute("DELETE FROM users")
  cursor.execute("DELETE FROM stores")
  cursor.execute("DELETE FROM items")

  # insert row (to add more rows use executemany)
  cursor.executemany("INSERT INTO users (id,username,password) VALUES (?,?,?)", users)

  # stores
  stores = [(1, "store-1"),
           (2, "store-2"),
           (3, "store-3"),
           ]
  cursor.executemany("INSERT INTO stores (id,name) VALUES (?,?)", stores)

  # items
  items = [(1, "item-1", 10.0, 1),
           (2, "item-2", 12.03, 2),
           (3, "item-3", 99, 2),
           ]
  cursor.executemany("INSERT INTO items (id,name,price,store_id) VALUES (?,?,?,?)", items)

  connection.commit()
  connection.close()


# If started as main module create temp data.db and insert users inside
if __name__ == "__main__":
  create_db('data.db')
