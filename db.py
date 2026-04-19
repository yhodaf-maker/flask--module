from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

_client = None
_db = None

def init_db(app):
    global _client, _db
    mongo_uri = os.getenv("MONGO_URI")
    _client = MongoClient(mongo_uri)
    _db = _client["prod"]
    app.config["DB"] = _db
    
def get_collection(name):
    return _db[name]