from setup_spotify_connection import get_spotify_query_object

spotify = get_spotify_query_object()

def get_artist_info(artist_name):
    res = spotify.search(q=artist_name,limit=1,type='artist')
    if len(res['artists']['items']) > 0:
        return res['artists']['items'][0]
    else:
        return {}
