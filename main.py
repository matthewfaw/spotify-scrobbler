from pprint import pprint
from datetime import datetime
from db.manager import post_to_database, get_top, get_distinct
from lastfm.contact import get_recent_tracks
from spotify.queries import get_genres

# print get_recent_tracks()
# print post_to_database()
# pprint([(x[0],get_genres(x[0])) for x in get_top('artist', 5)])

def update_music():
    '''Return False to trigger the canary

    Returns True if posting to database was successful
    '''
    recent = get_recent_tracks()
    print [str(track.track.artist) for track in recent]
    return post_to_database(recent)

# AWS Lamda stuff
def lambda_handler(event, context):
    print 'Adding new Spotify content at time %s' % (event['time'])
    try:
        if not update_music():
            raise Exception('Could not post all songs')
    except:
        print 'Check failed!'
        raise
    else:
        print('Check passed!')
        return event['time']
    finally:
        print 'Check complete at %s' % str(datetime.now())

