import time

import jwt
from flask import Flask, jsonify, request
from pymongo.collection import Collection
from bson import ObjectId

from api.database_connection import mongo_connection

from api.models.user_property import UserProperty
from api.models.auth_property import AuthProperty
from api.handlers.user_handle import UserHandle
from api.handlers.auth_handle import AuthHandle

from utils.auth_db_conn import auth_connected

from settings import settings

app = Flask(__name__)


# ...


# Helper function to convert ObjectId to string
def object_id_converter(o):
    if isinstance(o, ObjectId):
        return str(o)
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")


@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400
    else:
        user_collection = UserHandle.db_con_user()
        new_user = UserProperty(username=username, password=password)
        user_dict = new_user.to_dict()

        # Insert the new user into the collection and get the insert result
        insert_result = user_collection.insert_one(user_dict)

        # Add the string version of the ObjectId to the user_dict
        user_dict['_id'] = str(insert_result.inserted_id)
        print(user_dict)
        # Return the dictionary representation as JSON
        return jsonify(user_dict), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # merge username and password for a string
    sub = str(username + ' ' + password)
    # This is for expiration time set time break the Access Token
    current_time = int(time.time())
    expiration_time = current_time + 30
    # This merge sub + expiration_time to a dict to join for create Access Token (JWT)
    claims = {
        'sub': sub,
        'exp': expiration_time
    }

    # Check if username and password are provided
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    user_inf = UserHandle(username=username).get_user_info()

    # Check if user_inf exists and password matches
    if user_inf and user_inf.get('password') == password:
        auth_collection = AuthHandle.db_con_auth()
        encoded_data = jwt.encode(payload=claims,
                                  key=settings.AUTH_SECRET_KEY,
                                  algorithm="HS256")
        auth_token = AuthProperty(authToken=encoded_data)
        auth_token_dict = auth_token.to_dict()
        # Insert the new auth into the collection and get the insert auth
        insert_auth = auth_collection.insert_one(auth_token_dict)
        # Add the string version of the ObjectId to the auth_token_dict
        auth_token_dict['_id'] = str(insert_auth.inserted_id)

        # Delete ObjectID in the first user_inf inf was response from database
        user_inf = {k: object_id_converter(v) if isinstance(v, ObjectId) else v for k, v in user_inf.items()}
        return jsonify(
            {"User Name": user_inf['username'], "User Password": user_inf['password'],
             "Access Token": auth_token_dict['authToken']}), 200
    else:
        return jsonify({'message': 'User account does not exist!!!'}), 401


if __name__ == "__main__":
    app.run(debug=True)
