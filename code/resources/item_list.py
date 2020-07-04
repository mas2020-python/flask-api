from flask_restful import Resource
import tmpdb


class ItemList(Resource):
    def get(self):
        return {'items': tmpdb.items}, 200






