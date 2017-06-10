import os, sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

from pymongo import MongoClient
from db.models import get_song_model
from util.timehelper import unix_timestamp
from collections import defaultdict
from pprint import pprint

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

def time_is_valid(before, after):
    return before >= after

def get_counts(search, field, before='-1', after='-2'):
    '''
    Get frequency of field items between times before and after,
    where the items are retrieved from search, and 
    '''
    before = str(unix_timestamp()) if before == '-1' else before
    if not time_is_valid(before, after):
        print 'Invalid search range'
        return None
    x = defaultdict(lambda: 0)
    for song in search(before, after):
        x[song[field]] += 1
    return x

def basic_search(before='-1', after='-2'):
    before = str(unix_timestamp()) if before == '-1' else before
    return Song.find({ 'timestamp': { '$lt': before, '$gt': after } })

def get_top(field, n):
    '''
    field: The field over which to compute statistics
    n: The number of results to return
    '''
    x = defaultdict(lambda: 0)
    for song in Song.find().sort("timestamp"):
        x[song[field]] += 1
    topkeys = sorted(x, key=x.get, reverse=True)[0:n]
    topvals = [x[k] for k in topkeys]
    return zip(topkeys, topvals)

def get_distinct(field, before='-1', after='-2'):
    '''
    field: The field over which to compute statistics
    before: Unix timestamp before which to search
    after: Unix timestamp after which to search
    Returns the distinct field values that occur over the specified range
    '''
    x = []
    before = str(unix_timestamp()) if before == '-1' else before
    if before < after:
        print 'Invalid search range'
        return []
    for song in Song.find({ 'timestamp': { '$lt': before, '$gt': after } }).distinct(field):
        x.append(song)
    return x

# top = get_top('artist',5)
# for x in top:
    # print x[0], x[1]
# print get_distinct('artist')
