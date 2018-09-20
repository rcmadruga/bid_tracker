import copy
from flask_restful import reqparse, Resource
import localData as db

def abort_if_item_doesnt_exist(item_id):
    if item_id not in db.ITEMS:
        abort(404, message="Item {} doesn't exist".format(item_id))        

item_request_parser = reqparse.RequestParser()
item_request_parser.add_argument('winningOnly', type=int, location='args')
item_request_parser.add_argument('complete', type=int, location='args')

root_parser = reqparse.RequestParser()
root_parser.add_argument('item', type=dict)

item_post_parser = reqparse.RequestParser(bundle_errors=True)
item_post_parser.add_argument("name", type=str, location=('item'), required=True)

# Items
# Manage single item
class Item(Resource):
    def get(self, item_id):
        """
        Get item information
        ---
        parameters:
        - name: item_id
          in: path
          description: item identification
          type: string
          required: true
        - name: winningOnly
          in: query
          description: if set, only winning bid will be shown
          type: int
          required: false
          default: 0         
        - name: complete
          in: query
          description: if set, complete information about the bids will be shown
          type: int
          required: false
          default: 0  
        responses:
          200:
            description: Information about the item
            examples:
              items: {
                        "item": {
                            "name": "Item Nº 1",
                            "winning": "bid2",
                            "bids": [
                                {
                                    "bid_id": "bid1",
                                    "bid": {
                                        "item": "item1",
                                        "value": 500,
                                        "user": "user1"
                                    }
                                },
                                {
                                    "bid_id": "bid2",
                                    "bid": {
                                        "item": "item1",
                                        "value": 1000,
                                        "user": "user2"
                                    }
                                }
                            ]
                        }
                    }
        """
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
        """
        Delete a item from the system
        ---
        parameters:
        - name: item_id
          in: path
          description: Item identification
          type: string
          required: true
        responses:
          204:
            description: Item deleted           
        """
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
        """
        Get list of all items on the system
        ---
        responses:
          200:
            description: List of items
            examples:
              users: {
                        "item1": {
                            "item": {
                                "name": "Item Nº 1",
                                "winning": "bid2",
                                "bids": [
                                    "bid1",
                                    "bid2"
                                ]
                            }
                        },
                        "item2": {
                            "item": {
                                "name": "Item Nº 2",
                                "winning": null,
                                "bids": []
                            }
                        }
                    }
        """
        return db.ITEMS

    def post(self):
        """
        Add new item to system
        ---
        parameters:
        - name: name
          in: body
          description: item name
          type: string
          required: true
        responses:
          200:
            description: information about the new item created
            examples:
              item: { "name": "Item Nº 3" }
        """
        root_args = root_parser.parse_args()
        item_args = item_post_parser.parse_args(req=root_args)
        item_id = int(max(db.ITEMS.keys()).lstrip('item')) + 1
        item_id = 'item%i' % item_id

        item_args['winning'] = None
        item_args['bids'] = []
        db.ITEMS[item_id] = {'item': item_args}
        return db.ITEMS[item_id], 201
