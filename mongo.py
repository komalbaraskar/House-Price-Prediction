from pymongo import MongoClient
import os

client = MongoClient(os.getenv("MONGO_URI"))
db = client["house_price_db"]
collection = db["predictions"]