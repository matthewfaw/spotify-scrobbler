from setup_mongo_connection import get_songs_collection
from suggested_artists import get_related_artists
from artists import get_artist_info
from genres import get_genres
from save import save

mongo = get_songs_collection()

def get_all_artists():
    cur = mongo.aggregate([
        {"$group": {
            "_id": "$artist",
            "count": {"$sum":1}
            }},
        {"$sort": {
            "_id":1
            }}
        ])
    return cur

related_artist_dict = {}
genre_dict = {}
for doc in get_all_artists():
    artist = doc['_id']
    print artist
    info = get_artist_info(artist)
    if info != {}:
        artist_id = info['id']
        related_artist_dict[artist] = get_related_artists(artist_id=artist_id)
        genre_dict[artist] = get_genres(info=info)

save(related_artist_dict,'related_artists')
save(genre_dict,'genres')
