from flask import Blueprint, request, jsonify
import bcrypt
from DBAPIConfig.dbconfig import getDBConnection
import random
import jwt
import os

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@auth_blueprint.route('/signup', methods=['POST'])
def signup():
    try:
        connection = getDBConnection()
        cursor = connection.cursor()
        request_data = request.get_json()
        username = str(request_data['username'])
        password = str(request_data['password'])
        cursor.execute(
            f"SELECT COUNT(*) FROM users where username='{username}'")
        count = cursor.fetchone()[0]
        if count == 0:
            # hash password
            bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(bytes, salt)  # hash password

            user_id = ''
            for i in range(50):
                new_char = random.randint(0, 9)
                user_id += (str(new_char))  # create ID

            # insert user into db
            cursor.execute(
                f'INSERT INTO users (username,password,user_id) VALUES ("{username}","{hashed_password}","{user_id}")')
            connection.commit()

            jwt_token = jwt.encode({
                "user_id": user_id,
                "username": username
            }, os.environ.get("JWT_KEY"))  # create JWT Token

            return jsonify({'status': 'success', 'message': 'User Created', 'user': {
                'username': username,
                'user_id': user_id,
                "token": jwt_token
            }}), 201
        else:
            return jsonify({'status': 'fail', 'message': 'Username is taken. Pelase enter new credentials.'}), 409
    except:
        return jsonify({'status': 'fail', 'message': 'An unexpected error has occurred'}), 500


@auth_blueprint.route('/login', methods=['POST'])
def login():
    try:
        connection = getDBConnection()
        cursor = connection.cursor()
        request_data = request.get_json()
        username = str(request_data['username'])
        password = str(request_data['password'])
        cursor.execute(
            f"SELECT * FROM users where username='{username}'")
        user = cursor.fetchone()
        if user:
            userBytes = password.encode('utf-8')
            if bcrypt.checkpw(userBytes, user[1][2:-1].encode('utf-8')):
                jwt_token = jwt.encode(
                    {"user_id": user[2], "username": username}, os.environ.get("JWT_KEY"))
                return jsonify({'status': 'success', 'message': 'Login Successful', 'user': {
                    'username': username,
                    'user_id': user[2],
                }, "token": jwt_token}), 200
            else:
                return jsonify({'status': 'fail', 'message': 'Password incorrect'
                                }), 401
        else:
            return jsonify({'status': 'fail', 'message': 'No user with this username exists'}), 400

    except:
        return jsonify({'status': 'fail', 'message': 'An unexpected error has occurred'}), 500
