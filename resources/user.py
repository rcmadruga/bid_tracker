import copy
from flask_restful import reqparse, Resource
import localData as db

def abort_if_user_doesnt_exist(user_id):
    if user_id not in db.USERS:
        abort(404, message="User {} doesn't exist".format(user_id))

parser = reqparse.RequestParser()
parser.add_argument('name')

# Users
# Manage single user
class User(Resource):
    def get(self, user_id):
        abort_if_user_doesnt_exist(user_id)       
        return db.USERS[user_id]

    def delete(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        del db.USERS[user_id]
        del db.USERBIDS[user_id]
        return '', 204

    def put(self, user_id):
        args = parser.parse_args()
        user = {'user': args['user']}
        db.USERS[user_id] = user
        return user, 201

class UserItems(Resource):
    def get(self, user_id):
        abort_if_user_doesnt_exist(user_id)
        user_items = copy.deepcopy(db.USERS[user_id])
        
        # Get list of unique items that user bid on
        user_items['items_bid'] = list(set([db.BIDS[i]['bid']['item'] for i in db.USERBIDS[user_id]]))
        return user_items

# UserList
# shows a list of all users, and lets you POST to add new users
class UserList(Resource):
    def get(self):
        return db.USERS

    def post(self):
        args = parser.parse_args()
        user_id = int(max(db.USERS.keys()).lstrip('user')) + 1
        user_id = 'user%i' % user_id
        db.USERS[user_id] = {'user': args['name']}
        db.USERBIDS[user_id] = {}
        return db.USERS[user_id], 201
