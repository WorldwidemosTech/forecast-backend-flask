from flask import Blueprint, request
from bson.objectid import ObjectId
from src.config.database import property_forecast_collection
from src.utilities.exceptions.exceptionfactory import ExceptionFactory
from src.utilities.logging import get_logger
from src.utilities.respond import success
from src.utilities.schemahandler import SchemaHandler
from src.utilities.forecast.capital import Capital
from src.utilities.forecast.expense import Expense
from src.utilities.forecast.income import Income
from src.utilities.forecast.summary import Summary


property_forecast_bp = Blueprint(name="property_forecast", import_name=__name__)
logger = get_logger(__name__)
schema_handler = SchemaHandler()



@property_forecast_bp.route('/forecast/<string:property_id>', methods=['GET'])
def get_property(user_id: str, property_id: str):
    
    income = Income(user_id, property_id)
    income.execute()
    capital = Capital(user_id, property_id)
    capital.execute()
    expense = Expense(user_id, property_id)
    expense.execute()
    summary = Summary(user_id, property_id)
    summary.execute()

    response = property_forecast_collection.find({"user_id": ObjectId(user_id), "property_id":property_id})
    if not response:
        raise ExceptionFactory("").resource_not_found()
    response["_id"] = str(response["_id"])

    return success(response)
