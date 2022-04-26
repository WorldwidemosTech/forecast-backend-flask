import re
from flask import Blueprint, request
from src.config.logger import logger
from bson.objectid import ObjectId
import json
from src.utilities.respond import success
from src.utilities.exceptions.exceptionfactory import ExceptionFactory
from src.utilities.schemahandler import SchemaHandler
from src.db_config import user, property_general_data

property_bp = Blueprint(name="property", import_name=__name__)
schema_handler = SchemaHandler()


@property_bp.route('/property/<string:property_id>', methods=['GET'])
def get_property(user_id: str, property_id: str):
    """Gets an individual property general data."""

    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")

    response = property_general_data.find_one({'property_id': property_id,
                                            'user_id': user_id})
    logger.info(f"Data: {response}")
    if response == None:
        raise ExceptionFactory("Information not found").invalid_dict_parameter_value()
    return {"success": True, "message": "information_data", "body": json.loads(json.dumps(response))}


@property_bp.route('/property', methods=['GET'])
def get_property_list(user_id: str):
    """Gets a list of properties general data associated to user."""

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


@property_bp.route('/property', methods=['POST'])
def create_property(user_id: str):
    """Creates a property general data."""

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


@property_bp.route('/property/<string:property_id>', methods=['PUT'])
def update_property(user_id: str, property_id: str):
    """Updates individual property general data."""
   
    data = request.json
    schema_handler.validate_property_data(data)
    response = property_general_data.update_one({'user_id': user_id, '_id': ObjectId(property_id)}, {'$set': data})
    logger.info(f"Response: {response}")

    if response.modified_count < 1:
        raise ExceptionFactory("").documents_updated()

    return success("General data updated")
        


@property_bp.route('/property/<string:property_id>', methods=['DELETE'])
def delete_property(user_id: str, property_id: str):
    """Deletes a property general data."""

    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")
    response = property_general_data.delete_one({'user_id': user_id,
                                            '_id': ObjectId(property_id)})
    if response.deleted_count < 1:
        raise ExceptionFactory("").database_operation_failed()
        
    return success("information data deleted")
