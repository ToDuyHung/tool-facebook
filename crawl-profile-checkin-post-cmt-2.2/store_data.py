from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['user-profile-info']


def store_profile_into_mongo(info):
    user_info = db['user-profile']
    user_info.insert_one(info)

def store_tagged_user_into_mongo(user_post_info):
    user_post = db['user-tagged-posts']
    user_post.insert_one(user_post_info)
