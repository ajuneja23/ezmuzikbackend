import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials())
