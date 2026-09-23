from django.db import models
import pymongo
# from db_connection import db

# Create your models here.

client = pymongo.MongoClient("mongodb://localhost:27017")

db = client["user_db"]

Customer = db["Customer"]
