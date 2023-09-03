from DBAPIConfig.spotipy_config import spotify
from flask import Blueprint, request, jsonify
import jwt
import os
from DBAPIConfig.dbconfig import getDBConnection
spotify_blueprint = Blueprint('spotify', __name__, url_prefix='/spotify')


@spotify_blueprint.route('/song_data', methods=['POST'])
def getSongData():
    if request.method == 'POST':
        try:
            # validate token
            token = request.headers['Authorization']

            if not token or token.find("Bearer ") == -1:
                return jsonify({'status': 'fail', 'message': 'Not authorized to access this route'}), 401
            token = token[7:]

            payload = jwt.decode(token, os.environ.get(
                "JWT_KEY"), algorithms=['HS256'])

            user_id = payload["user_id"]

            connection = getDBConnection()
            cursor = connection.cursor()
            cursor.execute(
                f"SELECT COUNT(*) FROM users where user_id={user_id}")
            count = cursor.fetchone()
            if count == 0:
                return jsonify({'status': 'fail', 'message': 'Unauthorized to access this route'}), 401

            # process query
            query = str(request.get_json()['query'])
            items = spotify.search(q=query, limit=1)['tracks']['items']
            if len(items) == 0:
                return jsonify({'status': 'success', 'message': 'No song found'}), 200
            song_name = items[0]['name']
            song_id = items[0]['id']
            song_artist = items[0]['artists'][0]['name']
            audio_data = spotify.audio_analysis(song_id)['segments']
            loudness_data = []
            for datapoint in audio_data:
                loudness_data.append(
                    [datapoint['start'], datapoint['loudness_start']])  # [timestamp,loudness]
            # get similar artists
            artist_id = spotify.search(q=song_artist, type='artist', limit=1)[
                'artists']['items'][0]['id']
            related_artists = spotify.artist_related_artists(artist_id)[
                'artists']
            related_artist_names = []
            for i in range(len(related_artists)):
                related_artist_names.append(related_artists[i]['name'])
            return jsonify({'status': 'success', 'message': 'Data found', 'song_name': song_name, 'song_id': song_id, 'song_artist': song_artist, 'loudness_data': loudness_data, 'data_points': len(loudness_data), "related_artists": related_artist_names}), 200
        except:
            return jsonify({'status': 'fail', 'message': 'Error has occurred'}), 401
