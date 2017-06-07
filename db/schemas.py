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

def getSongSchema():
    return song_schema
