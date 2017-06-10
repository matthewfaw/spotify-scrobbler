import os, sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from pymongo import MongoClient
from db.models import get_song_model
from util.timehelper import unix_timestamp
from collections import defaultdict
from pprint import pprint

EMPTY_TIME = '-1'

# Environment variables
DB_URI = os.environ['db_uri']
DB_ID = os.environ['db_id'] #name of database

# Initialize connection with database
db = MongoClient(DB_URI)[DB_ID]
# Acquire Models
Song = get_song_model(db)

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

def _time_is_valid(before, after):
    return before >= after

def _get_counts(search, field, before=EMPTY_TIME, after=EMPTY_TIME):
    '''
    Get frequency of field items between times before and after,
    where the items are retrieved from search
    '''
    before = str(unix_timestamp()) if before == EMPTY_TIME else before
    if not _time_is_valid(before, after):
        print 'Invalid search range'
        return None
    x = defaultdict(lambda: 0)
    for song in search(before, after):
        x[song[field]] += 1
    return x

def _basic_search(before=EMPTY_TIME, after=EMPTY_TIME):
    return Song.find({ 'timestamp': { '$lt': before, '$gt': after } })

def get_top(field, n, before=EMPTY_TIME, after=EMPTY_TIME):
    '''
    Gets the top n field values from the database
    field: The field over which to compute statistics
    n: The number of results to return
    '''
    x = _get_counts(lambda b,a: _basic_search(b,a).sort('timestamp'), field, before, after)
    topkeys = sorted(x, key=x.get, reverse=True)[0:n]
    topvals = [x[k] for k in topkeys]
    return zip(topkeys, topvals)


def get_distinct(field, before=EMPTY_TIME, after=EMPTY_TIME):
    '''
    Gets the distinct values of field in the database
    field: The field over which to compute statistics
    before: Unix timestamp before which to search
    after: Unix timestamp after which to search
    Returns the distinct field values that occur over the specified range
    '''
    return sorted(_get_counts(_basic_search, field, before, after).keys())

# pprint(get_top('name',5))
# pprint(get_distinct('artist'))
