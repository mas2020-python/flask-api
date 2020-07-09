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
            items.append({'name': row[0], 'price': row[1]})
        connection.close()

        return items, 200






