import copy
from operator import itemgetter
from flask_restful import reqparse, Resource
import localData as db

root_parser = reqparse.RequestParser()
root_parser.add_argument('bid', type=dict)

bid_request_parser = reqparse.RequestParser(bundle_errors=True)
bid_request_parser.add_argument("item", type=str, location=('bid'), required=True, help="Item id of this bid has to be valid string")
bid_request_parser.add_argument("value", type=float, location=('bid'), required=True, help="Value must be a number")
bid_request_parser.add_argument("user", type=str, location=('bid'), required=True)

def abort_if_bid_doesnt_exist(bid_id):
    if bid_id not in db.BIDS:
        abort(404, message="Bid {} doesn't exist".format(bid_id))

def remove_bid_from_item(bid_id):
    item_id = db.BIDS[bid_id]['bid']['item']
    db.ITEMS[item_id]['item']['bids'].remove(bid_id)
    
    # update winning bid
    if db.ITEMS[item_id]['item']['winning'] == bid_id:
        tups = tuple((db.BIDS[b]['bid']['value'], b) for b in db.ITEMS[item_id]['item']['bids'])
        maxbid = max(tups,key=itemgetter(0))
        db.ITEMS[item_id]['item']['winning'] = maxbid[1]

# Bids
# Manage single bid
class Bid(Resource):
    def get(self, bid_id):
        """
        Get bid information
        ---
        parameters:
        - name: bid_id
          in: path
          description: bid identification
          type: string
          required: true
        responses:
          200:
            description: Information about the bid
            examples:
              bid: {
                        "bid_id": "bid1",
                        "bid": {
                            "item": "item1",
                            "value": 500,
                            "user": "user1"
                        }
                    }
        """
        abort_if_bid_doesnt_exist(bid_id)
        return db.BIDS[bid_id]

    def delete(self, bid_id):
        """
        Delete a bid from the system. If this bid is a winning bid for an item, a new winning bid will be selected for the item
        ---
        parameters:
        - name: bid_id
          in: path
          description: Bid identification
          type: string
          required: true
        responses:
          204:
            description: Bid deleted           
        """
        abort_if_bid_doesnt_exist(bid_id)
        
        # Get user_id
        user_id = db.BIDS[bid_id]['bid']['user']
        
        # remove from items an adjust winning ones
        remove_bid_from_item(bid_id)

        del db.BIDS[bid_id]     
        db.USERBIDS[user_id].remove(bid_id)       
        return '', 204

    def put(self, bid_id):
        args = bid_request_parser.parse_args()
        bid = {'bid': args['bid']}
        db.BIDS[bid_id] = bid
        return bid, 201

# BidList
# shows a list of all bids, and lets you POST to add new bids
class BidList(Resource):
    def get(self):
        """
        Get list of all bids on the system
        ---
        responses:
          200:
            description: List of bids
            examples:
              users: {
                        "bid1": {
                            "bid_id": "bid1",
                            "bid": {
                                "item": "item1",
                                "value": 500,
                                "user": "user1"
                            }
                        },
                        "bid2": {
                            "bid_id": "bid2",
                            "bid": {
                                "item": "item1",
                                "value": 1000,
                                "user": "user2"
                            }
                        }
                    }
        """
        return db.BIDS

    def post(self):
        """
        Add new bid to system
        ---
        parameters:
        - name: body
          in: body
          required: true
          schema:
            # Body schema with atomic property examples
            type: object
            properties:
              bid:
                type: object
                properties:
                  item:
                    type: string
                    example: item1
                    required: true
                  value:
                    type: float
                    example: 100.50
                    required: true
                  user:
                    type: string
                    required: true
                    example: user1                                              
        example:
          bid:
            item: item1
            value: 100000
            user: user1
        responses:
          200:
            description: information about the new bid created
            examples:
              bid: {
                        "bid_id": "bid3",
                        "bid": {
                            "item": "item1",
                            "value": 100000,
                            "user": "user1"
                        }
                    }
        """
        root_args = root_parser.parse_args()
        bid_args = bid_request_parser.parse_args(req=root_args)
        bid_id = int(max(db.BIDS.keys()).lstrip('bid')) + 1
        bid_id = 'bid%i' % bid_id

        # add bid
        db.BIDS[bid_id] = {'bid_id': bid_id,'bid': bid_args}
        db.USERBIDS[bid_args['user']].append(bid_id)
        
        # add to items
        it = db.ITEMS[bid_args['item']]
        bids = it['item']['bids']
        bids.append(bid_id)
        it['item']['bids'] = bids

        # check if this is a winning one
        if bid_args['value'] > db.BIDS[it['item']['winning']]['bid']['value']:
            it['item']['winning'] = bid_id       
        
        return db.BIDS[bid_id], 201

