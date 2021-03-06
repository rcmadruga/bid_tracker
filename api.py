from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flasgger import Swagger

from resources.user import User, UserItems, UserList
from resources.item import Item, ItemList
from resources.bid import Bid, BidList

app = Flask(__name__)
api = Api(app, prefix="/api/v1")
app.config['SWAGGER'] = {
    'title': 'BidTracker REST API',
    'uiversion': 3,
    'openapi': '3.0.1',
    'version': 'v1'
}

swagger = Swagger(app)

api.add_resource(UserList, '/users')
api.add_resource(User, '/users/<user_id>')
api.add_resource(UserItems, '/users/<user_id>/items')
api.add_resource(BidList, '/bids')
api.add_resource(Bid, '/bids/<bid_id>')
api.add_resource(ItemList, '/items')
api.add_resource(Item, '/items/<item_id>')

if __name__ == '__main__':
    app.run(debug=True)