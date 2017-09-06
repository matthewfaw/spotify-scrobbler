from setup_spotify_connection import get_spotify_query_object
from artists import get_artist_info

def get_genres(artist_name='', info={}):
    if info == {}:
        info = get_artist_info(artist_name)
        if info == {}: return []
    return info['genres']

# print get_genres('Arcade Fire')
