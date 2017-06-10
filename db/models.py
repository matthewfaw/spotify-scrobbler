from mongothon import create_model
from schemas import get_song_schema

def get_song_model(db):
    return create_model(get_song_schema(), db['song'])
