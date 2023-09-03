from flask import request, Blueprint, jsonify
from DBAPIConfig.dbconfig import getDBConnection
import jwt
import os
from datetime import datetime

query_blueprint = Blueprint('query', __name__, url_prefix='/query')


@query_blueprint.route('/', methods=['POST', 'GET'])
def makeQuery():
    if request.method == 'POST':
        try:
            token = request.headers['Authorization']
            if not token or token.find("Bearer ") == -1:
                return jsonify({'status': 'fail', 'message': 'Not authorized to access this route'}), 401
            token = token[7:]
            payload = jwt.decode(token, os.environ.get(
                "JWT_KEY"), algorithms=["HS256"])
            id = payload["user_id"]
            connection = getDBConnection()
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT COUNT(*) FROM users where user_id='{id}'")
            count = cursor.fetchone()
            if count == 0:
                return jsonify({'status': 'fail', 'message': 'Not authorized to access this route'}), 401
            request_data = request.get_json()
            user_id = str(payload["user_id"])
            query = str(request_data['query'])
            connection = getDBConnection()
            cursor = connection.cursor()
            searchdate = str(datetime.now())
            cursor.execute(
                f"INSERT INTO queries (query,searchdate,user_id) VALUES ('{query}','{searchdate}','{user_id}')")
            connection.commit()
            return jsonify({'status': 'success', 'message': 'Query processed', "query": {
                'input': query,
                'searchdate': searchdate,
                'user_id': user_id
            }}), 201
        except:
            return jsonify({'status': 'fail', 'message': 'An unexpected error has occurred'}), 500
    elif request.method == 'GET':
        try:
            token = request.headers["Authorization"]
            if not token or token.find("Bearer ") == -1:
                return jsonify({'status': 'fail', 'message': 'Not authorized to access this route'}), 401
            token = token[7:]
            payload = jwt.decode(token, os.environ.get(
                "JWT_KEY"), algorithms=['HS256'])
            user_name = str(payload["username"])

            connection = getDBConnection()
            cursor = connection.cursor()
            # validate token
            cursor.execute(
                f"SELECT COUNT(*) FROM users where username='{user_name}'")
            count = cursor.fetchone()
            if count == 0:
                return jsonify({'status': 'fail', 'message': 'Not authorized to access this route'}), 401

            # get query data
            cursor.execute(  # could just used user_id instead of username, but wanted to try joins
                f"select queries.searchdate,queries.query from queries left join users on queries.user_id=users.user_id where users.username='{user_name}'")
            queries = cursor.fetchall()
            filtered_queries = []
            for query in queries:
                filtered_queries.append({
                    "searchdate": query[0],
                    "query": query[1]
                })
            return jsonify({'status': 'success', 'message': 'Queries found', 'queries': filtered_queries, 'username': user_name}), 200

        except:
            return jsonify({'status': 'fail', 'message': 'An unexpected error has occurred'}), 500
