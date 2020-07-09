from flask_restful import Resource
import tmpdb
import sqlite3


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        result = cursor.execute(query)
        # read all rows in the table
        items = []
        for row in result:
            items.append({'id': row[0], 'name': row[1], 'price': row[2]})
        connection.close()

        return items, 200






