from pymongo import MongoClient
import os
from dotenv import load_dotenv

# 1. Loading environment variables from the .env file (for security)
load_dotenv()

# 2. Global variables to store the database connection
_client = None
_db = None

def init_db(app):
    global _client, _db
    # 3. Fetching the connection string (URI) from the environment variable
    mongo_uri = os.getenv("MONGO_URI")
    
    # 4. Creating the client and selecting the database named "prod"
    _client = MongoClient(mongo_uri)
    _db = _client["prod"]
    
    # 5. Storing the DB reference in the Flask app config for global access
    app.config["DB"] = _db
    
def get_collection(name):
    return _db[name]