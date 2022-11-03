from flask import Blueprint, request
from bson.objectid import ObjectId
from src.config.database import property_forecast_collection, property_general_data_collection
from src.utilities.exceptions.exceptionfactory import ExceptionFactory
from src.utilities.logging_ import get_logger
from src.utilities.json_toxlsx import fromJSON_toXLSX
from src.utilities.post_xlsx_s3 import post_to_s3
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
    # TODO: add error handling before to execute functions to validate user_id and property_id.
    
    income = Income(user_id, property_id)
    income.execute()
    capital = Capital(user_id, property_id)
    capital.execute()
    expense = Expense(user_id, property_id)
    expense.execute()
    summary = Summary(user_id, property_id)
    summary.execute()

    response = property_forecast_collection.find_one({"user_id": user_id, "property_id":property_id})
    file_name = str(response.get("_id"))
    url = f"https://financial-forecast.s3.us-east-2.amazonaws.com/{user_id}/{property_id}/{file_name}.xlsx"

    property_general_data_collection.update_one({"_id": ObjectId(property_id), "user_id": user_id},
                                                        {"$set": {"url_s3_forecast": url}})
    if not response:
        raise ExceptionFactory("").resource_not_found()

    try:
        json_forecast = response
        forecast_xlsx_document = fromJSON_toXLSX(json_forecast)
        posted_document_response = post_to_s3(forecast_xlsx_document,user_id, property_id, file_name)
        logger.info(f"S3 response: {posted_document_response['HTTPStatusCode']}.")
        
    except:
        raise ExceptionFactory("").forecast_not_processed()

    finally:
        return success({"body": json.loads(dumps(response))})
