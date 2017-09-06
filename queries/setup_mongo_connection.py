from ids import mongo_client_data as creds
from pymongo import MongoClient

def get_songs_collection():
    client = MongoClient(creds.uri)
    return client[creds.db][creds.collection]
