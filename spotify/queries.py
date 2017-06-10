import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

SPOTIFY_CLIENT_ID = os.environ['spotify_client_id']
SPOTIFY_CLIENT_SECRET = os.environ['spotify_client_secret']

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
s = Spotify(client_credentials_manager=client_credentials_manager)

def get_genres(query):
    return s.search(q=query, type='artist')['artists']['items'][0]['genres']

pprint(get_genres('Kanye West'))
