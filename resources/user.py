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
        """
        Get user information
        ---
        parameters:
        - name: user_id
          in: path
          description: User identification
          type: string
          required: false
        responses:
          200:
            description: Information about this user
            examples:
              user: { "name": "Albert" }
        """
        abort_if_user_doesnt_exist(user_id)       
        return db.USERS[user_id]

    def delete(self, user_id):
        """
        Delete a user from the system
        ---
        parameters:
        - name: user_id
          in: path
          description: User identification
          type: string
          required: true
        responses:
          204:
            description: User deleted           
        """
        abort_if_user_doesnt_exist(user_id)
        del db.USERS[user_id]
        del db.USERBIDS[user_id]
        return '', 204

    def put(self, user_id):
        """
        Update user information
        ---
        parameters:
        - name: user_id
          in: path
          description: User identification
          type: string
          required: true
        - name: name
          in: body
          description: Name of user
          type: string
          required: true          
        responses:
          201:
            description: Information about this user updated
            examples:
              user: { "name": "AlbertNew" }
        """
        args = parser.parse_args()
        user = {'name': args['name']}
        db.USERS[user_id] = user
        return user, 201

class UserItems(Resource):
    def get(self, user_id):
        """
        Get list of all items that this user bid on
        ---
        parameters:
        - name: user_id
          in: path
          description: User identification
          type: string
          required: true
        responses:
          200:
            description: List of items that this user bid on
            examples:
              user: { "name": "Albert", "items_bid": [ "item1" ] }
        """
        abort_if_user_doesnt_exist(user_id)
        user_items = copy.deepcopy(db.USERS[user_id])
        
        # Get list of unique items that user bid on
        user_items['items_bid'] = list(set([db.BIDS[i]['bid']['item'] for i in db.USERBIDS[user_id]]))
        return user_items

# UserList
# shows a list of all users, and lets you POST to add new users
class UserList(Resource):
    def get(self):
        """
        Get list of all users on the system
        ---
        responses:
          200:
            description: List of users
            examples:
              users: {     "user1": {         "name": "Albert"     },     "user2": {         "name": "Berry"     },     "user3": {        "name": "Constance"     } }
        """
        return db.USERS

    def post(self):
        """
        Add new user to system
        ---
        parameters:
        - name: name
          in: body
          description: User name
          type: string
          required: true
        responses:
          200:
            description: information about the new user created
            examples:
              user: { "name": "Albert" }
        """
        args = parser.parse_args()
        user_id = int(max(db.USERS.keys()).lstrip('user')) + 1
        user_id = 'user%i' % user_id
        db.USERS[user_id] = {'name': args['name']}
        db.USERBIDS[user_id] = {}
        return db.USERS[user_id], 201
