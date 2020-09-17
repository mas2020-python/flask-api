from flask_restful import Resource, reqparse
import logging
from utils.config import API_SRV


class Test(Resource):
    # Parse the args in the JSON payload to get all the arguments you specified here.
    parser = reqparse.RequestParser()

    def __init__(self):
        # Get the logger specified in the file
        self.logger = logging.getLogger(API_SRV.config['log']['default_logger'])

    def get(self):
        self.logger.debug("test method call!")
        return {'message': 'test OK!'}, 200

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
