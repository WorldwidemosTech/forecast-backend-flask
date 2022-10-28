from flask import Blueprint, request
from bson.objectid import ObjectId
from src.config.database import property_forecast_collection
from src.utilities.exceptions.exceptionfactory import ExceptionFactory
from src.utilities.logging_ import get_logger
from src.utilities.respond import success
from src.utilities.schemahandler import SchemaHandler
from src.utilities.forecast.capital import Capital
from src.utilities.forecast.expense import Expense
from src.utilities.forecast.income import Income
from src.utilities.forecast.summary import Summary
from bson.json_util import dumps
import json


property_forecast_bp = Blueprint(name="property_forecast", import_name=__name__)
logger = get_logger(__name__)
schema_handler = SchemaHandler()



@property_forecast_bp.route('/forecast/<string:property_id>', methods=['GET'])
def get_property(user_id: str, property_id: str):
    """Get the forecast with all the time-series values already claculated ."""
    
    income = Income(user_id, property_id)
    income.execute()
    capital = Capital(user_id, property_id)
    capital.execute()
    expense = Expense(user_id, property_id)
    expense.execute()
    summary = Summary(user_id, property_id)
    summary.execute()

    response = property_forecast_collection.find({"user_id": user_id, "property_id":property_id})
    response = dumps(response)
    if not response:
        raise ExceptionFactory("").resource_not_found()

    return success({"body": json.loads(response)})
