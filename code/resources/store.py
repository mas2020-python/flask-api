from flask_restful import Resource, reqparse
from models.store import StoreModel
from utils.config import API_SRV
import logging


class Store(Resource):
    def __init__(self):
        self.logger = logging.getLogger(API_SRV.config['log']['default_logger'])

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        # return a tuple a dict for the body and the code as a status code
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f'Store {name} is already there'}, 400
        # new Store
        store = StoreModel(name)
        try:
            store.save_to_db()
        except Exception as ex:
            self.logger.error(str(ex))
            return {'message': 'An error occurred while creating new store'}, 500

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if not store:
            return {'message': f'Store {name} is not present'}, 404
        try:
            store.delete()
        except Exception as ex:
            self.logger.error(str(ex))
            return {'message': f'An error occurred while deleting store {name}'}, 500


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
