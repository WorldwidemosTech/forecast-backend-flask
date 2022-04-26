import re
from flask import Blueprint, request
<<<<<<< HEAD
from src.config.logger import logger
from bson.objectid import ObjectId
import json
from src.utilities.respond import success
from src.utilities.exceptions.exceptionfactory import ExceptionFactory
=======
from bson.objectid import ObjectId
from src.config.database import property_general_data_collection
from src.utilities.exceptions.exceptionfactory import ExceptionFactory
from src.utilities.logging import get_logger
from src.utilities.respond import success
>>>>>>> 36ffa1d9616ab21c62d0b2f5f08e59c0db625e25
from src.utilities.schemahandler import SchemaHandler
from src.db_config import user, property_general_data

property_bp = Blueprint(name="property", import_name=__name__)
logger = get_logger(__name__)
schema_handler = SchemaHandler()


@property_bp.route('/property/<string:property_id>', methods=['GET'])
def get_property(user_id: str, property_id: str):
    """Gets an individual property general data."""
<<<<<<< HEAD

    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")

    response = property_general_data.find_one({'property_id': property_id,
                                            'user_id': user_id})
    logger.info(f"Data: {response}")
    if response == None:
        raise ExceptionFactory("Information not found").invalid_dict_parameter_value()
    return {"success": True, "message": "information_data", "body": json.loads(json.dumps(response))}
=======
    logger.info(f"Getting property: {property_id} general data for user: {user_id}.")
    response = property_general_data_collection.find_one({"_id": ObjectId(property_id), "user_id": user_id})
    if not response:
        raise ExceptionFactory("").resource_not_found()
    response["_id"] = str(response["_id"])
    return success(response)
>>>>>>> 36ffa1d9616ab21c62d0b2f5f08e59c0db625e25


@property_bp.route('/property', methods=['GET'])
def get_property_list(user_id: str):
    """Gets a list of properties general data associated to user."""
<<<<<<< HEAD

    logger.info(f"UserId: {user_id}")
    response = property_general_data.find({'user_id': user_id})
    list_items = []
    for i in response:
        i["_id"] = str(i["_id"])
        list_items.append(i)
    
    logger.info(f"List of items: {list_items}")
    if len(list_items) < 1:
        raise ExceptionFactory("Information not found").invalid_dict_parameter_value()
        
    return {"success": True, "message": "List of properties", "body": json.loads(json.dumps(list_items))}
=======
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
>>>>>>> 36ffa1d9616ab21c62d0b2f5f08e59c0db625e25


@property_bp.route('/property', methods=['POST'])
def create_property(user_id: str):
    """Creates a property general data."""
<<<<<<< HEAD

    logger.info(f"UserId: {user_id}")
    response = user.find_one({'user_id': user_id})
    logger.info(f"Response: {response}")
    if response == None:
        raise ExceptionFactory("").database_operation_failed()
    else:
        data = request.json
        data["user_id"] = user_id
        schema_handler.validate_property_data(data)
        property_general_data.insert_one(data)
        return success("General information created")
=======
    logger.info(f"Creating property general data for user {user_id}.")
    schema_handler.validate_property_general_data(request.json)

    data = request.json
    data["user_id"] = user_id

    response = property_general_data_collection.insert_one(data)
    if not response.acknowledged:
        raise ExceptionFactory("").database_operation_failed()
    return success({"inserted_id": str(response.inserted_id)})
>>>>>>> 36ffa1d9616ab21c62d0b2f5f08e59c0db625e25


@property_bp.route('/property/<string:property_id>', methods=['PUT'])
def update_property(user_id: str, property_id: str):
    """Updates individual property general data."""
<<<<<<< HEAD
   
    data = request.json
    schema_handler.validate_property_data(data)
    response = property_general_data.update_one({'user_id': user_id, '_id': ObjectId(property_id)}, {'$set': data})
    logger.info(f"Response: {response}")

    if response.modified_count < 1:
        raise ExceptionFactory("").documents_updated()

    return success("General data updated")
        
=======
    logger.info(f"Updating property: {property_id} general data for user {user_id}.")
    schema_handler.validate_property_general_data(request.json)

    response = property_general_data_collection.update_one({"_id": ObjectId(property_id), "user_id": user_id},
                                                           {"$set": request.json})
    if not response.acknowledged:
        raise ExceptionFactory("").database_operation_failed()
    return success({"modified_count": response.modified_count})
>>>>>>> 36ffa1d9616ab21c62d0b2f5f08e59c0db625e25


@property_bp.route('/property/<string:property_id>', methods=['DELETE'])
def delete_property(user_id: str, property_id: str):
    """Deletes a property general data."""
<<<<<<< HEAD

    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")
    response = property_general_data.delete_one({'user_id': user_id,
                                            '_id': ObjectId(property_id)})
    if response.deleted_count < 1:
        raise ExceptionFactory("").database_operation_failed()
        
    return success("information data deleted")
=======
    logger.info(f"Deleting property: {property_id} general data for user: {user_id}.")

    response = property_general_data_collection.delete_one({"_id": ObjectId(property_id), "user_id": user_id})

    if not response.acknowledged:
        raise ExceptionFactory("").database_operation_failed()
    return success({"deleted_count": response.deleted_count})
>>>>>>> 36ffa1d9616ab21c62d0b2f5f08e59c0db625e25
