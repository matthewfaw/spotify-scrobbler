import os, sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from pymongo import MongoClient
from db.models import getSongModel
from util.timehelper import unix_timestamp

# Environment variables
DB_URI = os.environ['db_uri']
DB_ID = os.environ['db_id'] #name of database

# Initialize connection with database
db = MongoClient(DB_URI)[DB_ID]
# Acquire Models
Song = getSongModel(db)

def _get_params(track, time):
    return {
            'artist': unicode(track.track.artist),
            'name': unicode(track.track.title),
            'album': unicode(track.album),
            'playback_date': unicode(track.playback_date),
            'timestamp': unicode(track.timestamp),
            'post_time': unicode(time),
            'username': unicode(track.track.network.username)
            }

def post_to_database(tracks=[]):
    currenttime = unix_timestamp()
    ret = True

    for track in tracks:
        params = _get_params(track, currenttime)
        newsong = Song(params)
        try:
            newsong.save()
        except:
            print 'Could not save song %s by artist %s from album %s for user %s' % (params['name'], params['artist'], params['album'], params['username'])
            ret = False
    return ret


