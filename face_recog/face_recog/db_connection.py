import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017")

db = client["user_db"]
