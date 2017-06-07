from mongothon import create_model
from schemas import getSongSchema

def getSongModel(db):
    return create_model(getSongSchema(), db['song'])
