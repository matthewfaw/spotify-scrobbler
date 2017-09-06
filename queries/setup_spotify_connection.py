from ids import spotify_client_ids as creds
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy import Spotify

def get_spotify_query_object():
    client_credentials_manager = SpotifyClientCredentials(client_id=creds.client_id, client_secret=creds.client_secret)
    sp = Spotify(client_credentials_manager=client_credentials_manager)
    return sp
