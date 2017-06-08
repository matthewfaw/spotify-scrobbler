# spotify-scrobbler

A script to collect and analyze my Spotify data.  My Spotify data is scrobbled to Last.FM, and I collect my data from there.
This script will be deployed to AWS Lambda and run every `100 minutes`, since songs are only added to listening history after
I listen to a song for at least 30 seconds, and  LastFM lets me retrieve the last 200 songs I've listened to. 

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
