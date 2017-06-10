# spotify-scrobbler

A script to collect and analyze my Spotify data.  My Spotify data is scrobbled to Last.FM, and I collect my data from there.
This script will be deployed to AWS Lambda and run every `100 minutes`, since songs are only added to listening history after
I listen to a song for at least 30 seconds, and  LastFM lets me retrieve the last 200 songs I've listened to. 

## API

- _main.py_
  - `  lambda_handler(event, context)`
    - AWS Lambda entrypoint
  - `update_music()`
    - Updates the database with music listened to since the last call
    - Returns whether or not the database post was successful
- __db__
  - _manager.py_
    - `post_to_database(tracks)`
      - Posts the tracks to the database
    - `get_top(field, n, before, after)`
      - Gets the top _n field_ values from the database
        - field: The database document field over which to compute statistics
        - _n_: The number of results to return
        - before: Unix timestamp before which to search
        - after: Unix timestamp after which to search
    - `get_distinct(field, before, after)`
      - Gets the distinct field values between times before and after
        - _field_: The database document field over which to compute statistics
        - before: Unix timestamp before which to search
        - after: Unix timestamp after which to search
  - _models.py_
    - `get_song_model(db)`
      - Gets the `mongothon` Song database model
        - db: The database object in `pymongo`
  - _schemas.py_
    - `get_song_schema()`
      - Gets the `mongothon` song Schema object
- __lastfm__
  - _contact.py_
    - `get_recent_tracks()`
      - Gets all songs listened to since the last check
- __spotify__
  - _queries.py_
    - `get_genres(query, qtype)`
      - Gets the genres associated with the query
        - query: The search term
        - qtype: The type of object to search for
          - Currently, only works for 'artist'.  This is an error on Spotify's [end](https://github.com/spotify/web-api/issues/157)
          
## Entry point
`main.py`

Note that this script requires several environment variables that must be initialized.

## Deploying to AWS Lambda

First, run `zip -r lambda.zip . -x@exclude.lst` in the project root.
Then, upload the resulting zip file.

## Primary dependencies:
- [pymongo](http://api.mongodb.com/python/current/api/pymongo/)
- [mongothon](https://github.com/gamechanger/mongothon)
- [pylast](https://github.com/pylast/pylast)
- [spotipy](spotipy.readthedocs.io)
