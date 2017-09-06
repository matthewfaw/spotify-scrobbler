import json
from setup_spotify_connection import get_spotify_query_object
from artists import get_artist_info

spotify = get_spotify_query_object()

def get_related_artists(artist_name='', artist_id=''):
    if artist_name == '' and artist_id == '': return []
    if artist_id == '':
        info = get_artist_info(artist_name)
        if info == {}: return []
        artist_id = info['id']
    ret = spotify.artist_related_artists(artist_id)['artists']
    # return ret
    return [e['name'] for e in ret]

# related = get_related_artists('Arcade Fire')
# print json.dumps(related,sort_keys=True,indent=4)
