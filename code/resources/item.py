from flask import request
from flask_restful import Resource, reqparse
import tmpdb
from flask_jwt import jwt_required
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

    #TODO: implement post saving into db
    def post(self, name):
        # search if an item with the same name doesn't exist ('is not None' can be omitted)
        if next(filter(lambda x: x['name'] == name, tmpdb.items), None) is not None:
            return {'message': f'an item with the same name \'{name}\' already exists'}, 400

        # get the JSON payload: if the body is not JSON or the content header is not application/JSON we get an error
        # if you pass force=TRUE you disabled the application/JSON content header to be mandatory
        data = request.get_json()
        # name is a param from the request, price is in the JSON body
        item = {'name': name, 'price': data['price']}
        tmpdb.items.append(item)
        # return item with the 201 http code
        return item, 201

    # Update a single element
    def put(self, name):
        # search for the name item (using the pattern of the error first approach)
        item = next(filter(lambda x: x['name'] == name, tmpdb.items), None)
        if not item:
            # return not found
            return {'message': 'item not found'}, 404

        # if OK, parse args
        data = Item.parser.parse_args()
        # dict update to modify its content receiving a dict input
        item.update(data)
        # return the item updated
        return item


