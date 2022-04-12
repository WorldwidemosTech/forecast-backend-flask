import pymongo
import os
from dotenv import load_dotenv
import sys

load_dotenv('.env')

DB_USER = os.environ.get("MONGO_DB_USER")
DB_PASSWORD = os.environ.get("MONGO_DB_PASS")
DB_URL = os.environ.get("MONGO_DB_URL")
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME')



# Pymongo Client Instance
client = pymongo.MongoClient(f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster0.w32f1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# Smartcast Main Database Instance
database = client[MONGO_DB_NAME]


# Smartcast Collections
user = database["user_info"]
property_information = database["property_information"]
property_general_data = database["property_general_data"]