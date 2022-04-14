import os

import pymongo
from dotenv import load_dotenv

load_dotenv('.env')

DB_USER = os.environ.get("MONGO_DB_USER", "smartcast_admin")
DB_PASSWORD = os.environ.get("MONGO_DB_PASS", "mCjTLbC1EHgyJUaq")
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', "financial_forecast")

# Pymongo Client Instance
client = pymongo.MongoClient(
    f"mongodb+srv://{DB_USER}:{DB_PASSWORD}@cluster0.w32f1.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

# Smartcast Main Database Instance
database = client[MONGO_DB_NAME]

# Smartcast Collections
user = database["user_info"]
property_information = database["property_information"]
property_general_data = database["property_general_data"]
