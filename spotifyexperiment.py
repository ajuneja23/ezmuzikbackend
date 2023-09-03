from DBAPIConfig.spotipy_config import spotify
import bcrypt
"""result = spotify.search(q='melo ball', limit=1)
id = result['tracks']['items'][0]['id']
print(id)
analysis = spotify.audio_analysis(id)
parsed_analysis = {}
for key in analysis:
    if key != 'codestring':
        parsed_analysis[key] = analysis[key]
print(parsed_analysis['segments'][0])
for element in parsed_analysis['segments']:
    print(element)
    print('a')
    print(element['start'])
    print(element['loudness_start'])
"""

id = spotify.search(q='melo ball 1', limit=1)['tracks']['items'][0]['id']
analysis = spotify.audio_analysis(id)
artist = spotify.search(q='melo ball 1', limit=1)[
    'tracks']['items'][0]['artists'][0]['name']

artist = spotify.search(q=artist, type='artist', limit=1)

id = artist['artists']['items'][0]['id']

artists = spotify.artist_related_artists(id)['artists']

names = []
for i in range(len(artists)):
    names.append(artists[i]['name'])
print(names)
