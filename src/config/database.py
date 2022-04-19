import pymongo

from src.config.config import mongo_user
from src.config.config import mongo_password
from src.config.config import mongo_database

# Pymongo Client Instance
mongo = pymongo.MongoClient(
    f"mongodb+srv://{mongo_user}:{mongo_password}@cluster0.w32f1.mongodb.net/{mongo_database}?retryWrites=true&w=majority")

# Smartcast Collections
user_info_collection = mongo[mongo_database].user_info
property_general_data_collection = mongo[mongo_database].property_general_data
property_information_collection = mongo[mongo_database].property_information
property_scenarios_collection = mongo[mongo_database].property_scenarios

