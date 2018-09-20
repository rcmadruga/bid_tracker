import copy
from flask_restful import reqparse, Resource
import localData as db

def abort_if_bid_doesnt_exist(bid_id):
    if bid_id not in db.BIDS:
        abort(404, message="Bid {} doesn't exist".format(bid_id))

root_parser = reqparse.RequestParser()
root_parser.add_argument('bid', type=dict)

bid_request_parser = reqparse.RequestParser(bundle_errors=True)
bid_request_parser.add_argument("item", type=str, location=('bid'), required=True, help="Item id of this bid has to be valid string")
bid_request_parser.add_argument("value", type=float, location=('bid'), required=True, help="Value must be a number")
bid_request_parser.add_argument("user", type=str, location=('bid'), required=True)

# Bids
# Manage single bid
class Bid(Resource):
    def get(self, bid_id):
        abort_if_bid_doesnt_exist(bid_id)
        return db.BIDS[bid_id]

    def delete(self, bid_id):
        abort_if_bid_doesnt_exist(bid_id)
        user = db.BIDS[bid_id]['bid']['user']
        del db.BIDS[bid_id]
        del db.USERBIDS[user][bid_id]
        # TODO update winning bid on items if this bid is a winning one
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
        return db.BIDS

    def post(self):
        root_args = root_parser.parse_args()
        bid_args = bid_request_parser.parse_args(req=root_args)
        bid_id = int(max(db.BIDS.keys()).lstrip('bid')) + 1
        bid_id = 'bid%i' % bid_id
        db.BIDS[bid_id] = {'bid_id': bid_id,'bid': bid_args}
        it = db.ITEMS[bid_args['item']]
        bids = it['item']['bids']
        bids.append(bid_id)
        it['item']['bids'] = bids
        if bid_args['value'] > db.BIDS[it['item']['winning']]['bid']['value']:
            it['item']['winning'] = bid_id
        db.USERBIDS[bid_args['user']].append(bid_id)
        return db.BIDS[bid_id], 201

