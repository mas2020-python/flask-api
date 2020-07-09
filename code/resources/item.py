from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.item import ItemModel


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
        item = ItemModel.find_by_name(name)
        if item:
            # return a json representation for the API
            return item.json()
        return {'message': 'item not found'}, 404

    def post(self, name):
        # search if an item with the same name doesn't exist ('is not None' can be omitted)
        if ItemModel.find_by_name(name):
            return {'message': f'an item with the same name \'{name}\' already exists'}, 400

        # get the JSON payload: if the body is not JSON or the content header is not application/JSON we get an error
        # if you pass force=TRUE you disabled the application/JSON content header to be mandatory
        data = request.get_json()
        # name is a param from the request, price is in the JSON body
        item = ItemModel(name, data['price'])

        # save into db
        try:
            item.insert()
        except Exception as e:
            return {'message': f"an error occurred during saving an item: {e}"}, 500

        # return item with the 201 http code
        return item.json(), 201

    # Update a single element
    def put(self, name):
        # search for the name item (using the pattern of the error first approach)
        item_model: ItemModel = ItemModel.find_by_name(name)
        if not item_model:
            # return not found
            return {'message': 'item not found'}, 404

        # if OK, parse args to get the new price
        data = Item.parser.parse_args()
        try:
            # update db
            item_model.price = data['price']
            item_model.insert()
        except Exception as e:
            return {'message': f"an error occurred during saving an item: {e}"}, 500

        # return item with the 201 http code
        return "", 204

    # Delete a single element
    def delete(self, name):
        # search for the name item (using the pattern of the error first approach)
        item: ItemModel = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'deleted'}, 202
        # return not found
        return {'message': 'item not found'}, 404