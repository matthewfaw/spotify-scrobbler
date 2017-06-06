# from __future__ import print_function
import pylast, os, time
from pymongo import MongoClient
from datetime import datetime
from models import getSongModel

# Constants
MAX_NUM_ITEMS = 200

# Get environment variables
API_KEY = os.environ['api_key']
API_SECRET = os.environ['api_secret']
USERNAME = os.environ['username']
FREQUENCY = int(os.environ['frequency']) # in minutes
DB_URI = os.environ['db_uri']
DB_ID = os.environ['db_id'] #name of database

# Initialize connection with database
db = MongoClient(DB_URI)[DB_ID]
# Acquire Models
Song = getSongModel(db)

# Initialize connection with Last.FM
network = pylast.LastFMNetwork(api_key=API_KEY, 
                               api_secret=API_SECRET,
                               username=USERNAME)
user = network.get_user(USERNAME)

def get_db():
    return db

def unix_timestamp(delta_minutes=0):
    return int(time.time()) + delta_minutes*60

def get_recent_tracks():
    '''
    Gets all songs listened to since the last check
    '''
    return user.get_recent_tracks(limit=MAX_NUM_ITEMS, time_from=unix_timestamp(-FREQUENCY))

def post_to_database(tracks=[]):
    currenttime = unix_timestamp()
    for track in tracks:
        newsong = Song({
            "artist": unicode(track.track.artist),
            "name": unicode(track.track.title),
            "album": unicode(track.album),
            "playback_date": unicode(track.playback_date),
            "timestamp": unicode(track.timestamp),
            "post_time": unicode(currenttime)
        })
        newsong.save()
    return True

post_to_database(get_recent_tracks())
# print get_recent_tracks()

def update_music():
    '''Return False to trigger the canary

    Returns True if posting to database was successful
    '''
    recent = get_recent_tracks()
    print [str(track.track.artist) for track in recent]
    return post_to_database(get_recent_tracks())

# AWS Lamda stuff
def lambda_handler(event, context):
    print('Checking {} at {}...'.format(SITE, event['time']))
    try:
        if not validate(urlopen(SITE).read()):
            raise Exception('Validation failed')
    except:
        print('Check failed!')
        raise
    else:
        print('Check passed!')
        return event['time']
    finally:
        print('Check complete at {}'.format(str(datetime.now())))

