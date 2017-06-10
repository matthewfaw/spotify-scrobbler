from datetime import datetime
from db.manager import post_to_database
from lastfm.contact import get_recent_tracks

print get_recent_tracks()
print post_to_database()

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

