import os

from dotenv import load_dotenv

load_dotenv('.env')

# TODO: change db keys to env variables

mongo_user = os.environ.get("MONGO_DB_USER")
mongo_password = os.environ.get("MONGO_DB_PASS")
mongo_database = os.environ.get("MONGO_DB_NAME")

# mongo_user =  "smartcast_admin"
# mongo_password = "mCjTLbC1EHgyJUaq"
# mongo_database = "financial_forecast"
