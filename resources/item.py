import copy
from flask_restful import reqparse, Resource
import localData as db

def abort_if_item_doesnt_exist(item_id):
    if item_id not in db.ITEMS:
        abort(404, message="Item {} doesn't exist".format(item_id))        

item_request_parser = reqparse.RequestParser()
item_request_parser.add_argument('winningOnly', type=int, location='args')
item_request_parser.add_argument('complete', type=int, location='args')

# Items
# Manage single item
class Item(Resource):
    def get(self, item_id):
        abort_if_item_doesnt_exist(item_id)
        args = item_request_parser.parse_args()
        # deal with winningOnly flag
        if 'winningOnly' in args and args['winningOnly'] == 1:
            item = copy.deepcopy(db.ITEMS[item_id])
            del item['item']['bids']
            return item
        # deal with complete flag
        if 'complete' in args and args['complete'] == 1:
            item = copy.deepcopy(db.ITEMS[item_id])
            complete_bids = [db.BIDS[i] for i in item['item']['bids']]
            item['item']['bids'] = complete_bids
            return item
        return db.ITEMS[item_id]

    def delete(self, item_id):
        abort_if_item_doesnt_exist(item_id)
        del db.ITEMS[item_id]
        return '', 204

    def put(self, item_id):
        args = parser.parse_args()
        item = {'item': args['item']}
        db.ITEMS[item_id] = item
        return item, 201

# ItemList
# shows a list of all items, and lets you POST to add new items
class ItemList(Resource):
    def get(self):
        return db.ITEMS

    def post(self):
        args = parser.parse_args()
        item_id = int(max(db.ITEMS.keys()).lstrip('item')) + 1
        item_id = 'item%i' % item_id
        db.ITEMS[item_id] = {'item': args['item']}
        return db.ITEMS[item_id], 201
