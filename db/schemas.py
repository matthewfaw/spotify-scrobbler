from mongothon import Schema

# name: song title
# playback_date: time song was played on Spotify
# timestamp: The Unix UTC time played on Spotify
# post_time: The time that the script was run
song_schema = Schema({
    'artist': {'type': unicode, 'required': True},
    'name': {'type': unicode, 'required': True},
    'album': {'type': unicode, 'required': True},
    'playback_date': {'type': unicode, 'required': True},
    'timestamp': {'type': unicode, 'required': True},
    'post_time': {'type': unicode, 'required': True},
    'username': {'type': unicode, 'required': True},
    })

artist_schema = Schema({
    'name': {'type': unicode, 'required': True},
    'genres': [{'type': unicode}],
    })
album_schema = Schema({
    'name': {'type': unicode, 'required': True},
    'artist': {'type': unicode, 'required': True}
    })
song_schema = Schema({
    'name': {'type': unicode, 'required': True},
    'album': {'type': album_schema}
    })

stats_schema = Schema({
    'top_artists': [{'type': artist_schema}],
    'top_albums': [{'type': album_schema}],
    'top_songs': [{'type': song_schema}],
    'top_genres': [{'type': unicode}],
    })

def get_song_schema():
    return song_schema
