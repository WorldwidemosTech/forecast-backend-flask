from flask import Blueprint, request
from bson.objectid import ObjectId
from src.config.database import property_general_data_collection
from src.utilities.exceptions.exceptionfactory import ExceptionFactory
from src.utilities.logging import get_logger
from src.utilities.respond import success
from src.utilities.schemahandler import SchemaHandler


property_bp = Blueprint(name="property", import_name=__name__)
logger = get_logger(__name__)
schema_handler = SchemaHandler()


@property_bp.route('/property/<string:property_id>', methods=['GET'])
def get_property(user_id: str, property_id: str):
    """Gets an individual property general data."""
    logger.info(f"Getting property: {property_id} general data for user: {user_id}.")
    response = property_general_data_collection.find_one({"_id": ObjectId(property_id), "user_id": user_id})
    if not response:
        raise ExceptionFactory("").resource_not_found()
    response["_id"] = str(response["_id"])
    return success(response)


@property_bp.route('/property', methods=['GET'])
def get_property_list(user_id: str):
    """Gets a list of properties general data associated to user."""
    logger.info(f"Getting properties general data for user: {user_id}.")

    response = property_general_data_collection.find({"user_id": user_id})
    response = list(response)

    if not response:
        raise ExceptionFactory("").resource_not_found()

    properties = []
    for item in response:
        item["_id"] = str(item["_id"])
        properties.append(item)

    return success(properties)


@property_bp.route('/property', methods=['POST'])
def create_property(user_id: str):
    """Creates a property general data."""
    logger.info(f"Creating property general data for user {user_id}.")
    schema_handler.validate_property_general_data(request.json)

    data = request.json
    data["user_id"] = user_id

    response = property_general_data_collection.insert_one(data)
    if not response.acknowledged:
        raise ExceptionFactory("").database_operation_failed()
    return success({"inserted_id": str(response.inserted_id)})


@property_bp.route('/property/<string:property_id>', methods=['PUT'])
def update_property(user_id: str, property_id: str):
    """Updates individual property general data."""
    logger.info(f"Updating property: {property_id} general data for user {user_id}.")
    schema_handler.validate_property_general_data(request.json)

    response = property_general_data_collection.update_one({"_id": ObjectId(property_id), "user_id": user_id},
                                                           {"$set": request.json})
    if not response.acknowledged:
        raise ExceptionFactory("").database_operation_failed()
    return success({"modified_count": response.modified_count})


@property_bp.route('/property/<string:property_id>', methods=['DELETE'])
def delete_property(user_id: str, property_id: str):
    """Deletes a property general data."""
    logger.info(f"Deleting property: {property_id} general data for user: {user_id}.")

    response = property_general_data_collection.delete_one({"_id": ObjectId(property_id), "user_id": user_id})

    if not response.acknowledged:
        raise ExceptionFactory("").database_operation_failed()
    return success({"deleted_count": response.deleted_count})
