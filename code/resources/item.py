from flask import request
from flask_restful import Resource, reqparse
import tmpdb
from flask_jwt import jwt_required, current_identity
import sqlite3


class Item(Resource):
    # Parse the args in the JSON payload to get only price. It is a static variable
    # for the class
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be empty!")

    @jwt_required()
    def get(self, name):
        user = current_identity
        # search item on db
        item = Item.find_by_name(name)
        if item:
            return item
        return {'message': 'item not found'}, 404

    @classmethod
    # Search an item by name
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        # get the first row from a result set
        row = result.fetchone()
        connection.close()
        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        return None

    @classmethod
    def insert(cls, item):
        # save into db
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        # save into db
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price = ? WHERE name = ?"
        cursor.execute(query, (item['price'], item['name']))
        connection.commit()
        connection.close()

    def post(self, name):
        # search if an item with the same name doesn't exist ('is not None' can be omitted)
        if Item.find_by_name(name):
            return {'message': f'an item with the same name \'{name}\' already exists'}, 400

        # get the JSON payload: if the body is not JSON or the content header is not application/JSON we get an error
        # if you pass force=TRUE you disabled the application/JSON content header to be mandatory
        data = request.get_json()
        # name is a param from the request, price is in the JSON body
        item = {'name': name, 'price': data['price']}

        # save into db
        try:
            Item.insert(item)
        except Exception as e:
            return {'message': f"an error occurred during saving an item: {e}"}, 500

        # return item with the 201 http code
        return item, 201

    # Update a single element
    def put(self, name):
        # search for the name item (using the pattern of the error first approach)
        item = Item.find_by_name(name)
        if not item:
            # return not found
            return {'message': 'item not found'}, 404

        # if OK, parse args to get the new price
        data = Item.parser.parse_args()
        try:
            # update db
            Item.update({'price': data['price'], 'name': name})
        except Exception as e:
            return {'message': f"an error occurred during saving an item: {e}"}, 500

        # return item with the 201 http code
        return "", 204



