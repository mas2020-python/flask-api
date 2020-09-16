from flask_restful import Resource
from flask import request
from models.store import StoreModel
from utils.config import API_SRV
import logging
import traceback


class Store(Resource):
    def __init__(self):
        self.logger = logging.getLogger(API_SRV.config['log']['default_logger'])

    def get(self, _id):
        store = StoreModel.find_by_id(_id)
        if store:
            return store.json()
        # return a tuple a dict for the body and the code as a status code
        return {'message': 'Store not found'}, 404

    def delete(self, _id):
        store: StoreModel = StoreModel.find_by_id(_id)
        if not store:
            return {'message': f'Store with id {_id} is not present'}, 404
        try:
            store.delete_from_db()
            return {}, 204
        except Exception as ex:
            self.logger.error(traceback.format_exc())
            return {'message': f'An error occurred while deleting store with id {_id}'}, 500


class StoreList(Resource):
    def __init__(self):
        self.logger = logging.getLogger(API_SRV.config['log']['default_logger'])

    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}

    @property
    def post(self):
        try:
            data = request.json
            if StoreModel.find_by_name(data['name']):
                return {'message': f'Store {data["name"]} is already there'}, 400
            # new Store
            store = StoreModel(data['name'])
            store.save_to_db()
            return {'store': store.json()}, 200
        except Exception as ex:
            self.logger.error(traceback.format_exc())
            return {'message': 'An error occurred, refer to the system administrator to read log file'}, 500
