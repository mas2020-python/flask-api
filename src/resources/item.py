from flask_restful import Resource, reqparse, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_claims,
    jwt_optional,
    get_jwt_identity,
    fresh_jwt_required
)
from models.item import ItemModel
import logging
from utils.config import API_SRV


class Item(Resource):
    # Parse the args in the JSON payload to get all the arguments you specified here.
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be empty!")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id")

    def __init__(self):
        # Get the logger specified in the file
        self.logger = logging.getLogger(API_SRV.config['log']['default_logger'])

    @jwt_required
    def get(self, name):
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

        # parse the arguments in the JSON payload
        data = Item.parser.parse_args()
        # name is a param from the request, price is in the JSON body
        # item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)  # using dict expansion

        # save into db
        try:
            item.insert()
        except Exception as e:
            self.logger.error(str(e))
            return {'message': f"An error occurred during saving an item, read log for major details"}, 500

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
            item_model.store_id = data['store_id']  # we can change the store_is as well
            item_model.insert()
        except Exception as e:
            return {'message': f"an error occurred during saving an item: {e}"}, 500

        # return item with the 201 http code
        return "", 204

    @fresh_jwt_required
    def delete(self, name):
        """
        This method delete the item from database. This is an example of using claim also to
        determine if the user has the right privilege for this operation.
        This is also need to receive a fresh token to let user executes the operation.
        :param name: item name to delete
        :return: json response
        """
        # get the claims from the token
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privileges are required for this operation'}, 401

        # search for the name item (using the pattern of the error first approach)
        item: ItemModel = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'deleted'}, 202
        # return not found
        return {'message': 'item not found'}, 404


class ItemList(Resource):
    def __init__(self):
        # Get the logger specified in the file
        self.logger = logging.getLogger(API_SRV.config['log']['default_logger'])

    @jwt_optional
    def get(self):
        """
        Get items from DB. It is possible to pass a query string with this syntax: ?name=value
        The application will apply a like query filter to the name, as if you wrote 'name like value%' in SQL language
        :return:
        """
        self.logger.debug(f"/items args: {request.args}")
        # get the identity, if it exists it means the user is authenticated. If the jwt is not present
        # the method a subset of information
        user_id = get_jwt_identity()
        # filter by the query string
        if not request.args['name']:
            items = [item.json() for item in ItemModel.find_all()]
        else:
            items = [item.json() for item in ItemModel.find_by_name_like(request.args['name'])]
        # create the answer based on the token or not
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in'
        }

        # old code
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items"
        # result = cursor.execute(query)
        # # read all rows in the table
        # items = []
        # for row in result:
        #     items.append({'id': row[0], 'name': row[1], 'price': row[2]})
        # self.logger.info(f"items get back: {len(items)}")
        # connection.close()
        #
        # return items, 200
