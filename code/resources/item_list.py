from flask_restful import Resource
import logging
from models.item import ItemModel

class ItemList(Resource):
    def __init__(self):
        # Get the logger specified in the file
        self.logger = logging.getLogger("sampleLogger")

    def get(self):
        # using the list comprehension
        return {'items': [item.json() for item in ItemModel.query.all()]}
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






