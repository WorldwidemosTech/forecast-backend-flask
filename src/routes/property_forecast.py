from flask import Blueprint, request
from bson.objectid import ObjectId
from src.config.database import property_general_data_collection
from src.utilities.exceptions.exceptionfactory import ExceptionFactory
from src.utilities.logging import get_logger
from src.utilities.respond import success
from src.utilities.schemahandler import SchemaHandler

property_forecast_bp = Blueprint(name="property_forecast", import_name=__name__)
logger = get_logger(__name__)
schema_handler = SchemaHandler()



@property_forecast_bp.route('/forecast/<string:property_id>', methods=['GET'])
def get_property(user_id: str, property_id: str):
    """Gets an individual property general data."""
    ...

@property_forecast_bp.route('/forecast', methods=['POST'])
def create_property(user_id: str):
    """Creates a property general data."""
    ...


@property_forecast_bp.route('/forecast/<string:property_id>', methods=['DELETE'])
def delete_property(user_id: str, property_id: str):
    """Deletes a property general data."""
    ...
