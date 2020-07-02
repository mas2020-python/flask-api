from flask_restful import Resource
import tmpdb


class Item(Resource):
    def get(self, name):
        for i in tmpdb.items:
            if i['name'] == name:
                return i
        # return item is not found with the 404 http code
        return {'message': 'item not found'}, 404

    def post(self, name):
        # name is from the request, price is a default
        item = {'name': name, 'price': 12}
        tmpdb.items.append(item)
        # return item with the 201 http code
        return item, 201





