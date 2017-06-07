import os, sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import pylast
from util.timehelper import unix_timestamp

# Constants
MAX_NUM_ITEMS = 200

# Get environment variables
API_KEY = os.environ['api_key']
API_SECRET = os.environ['api_secret']
USERNAME = os.environ['username']
FREQUENCY = int(os.environ['frequency']) # in minutes

# Initialize connection with LastFM
network = pylast.LastFMNetwork(api_key=API_KEY, 
                               api_secret=API_SECRET,
                               username=USERNAME)
user = network.get_user(USERNAME)

def get_recent_tracks():
    '''
    Gets all songs listened to since the last check
    '''
    return user.get_recent_tracks(limit=MAX_NUM_ITEMS, time_from=unix_timestamp(-FREQUENCY))
