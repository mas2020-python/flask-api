from flask import Flask
from flask_restful import Resource, Api
from resources.item import Item

"""
Using flask_restful jsonify for object that are not dictionary is not needed cause flask restful
do it for us.
"""

# creating main app
app = Flask(__name__)
api = Api(app)


# Add resources and binding with the HTTP URL
api.add_resource(Item, '/item/<string:name>')

# run the test server
app.run(port=5000)


