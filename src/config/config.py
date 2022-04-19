import os

from dotenv import load_dotenv

load_dotenv('.env')

mongo_user = os.environ.get("MONGO_DB_USER", "smartcast_admin")
mongo_password = os.environ.get("MONGO_DB_PASS", "mCjTLbC1EHgyJUaq")
mongo_database = os.environ.get('MONGO_DB_NAME', "financial_forecast")
