import json

from flask import Blueprint, request

from src.config.logger import logger
from src.config.database import property_information_collection
from src.config.database import user_info_collection
from src.utilities.respond import success
from src.utilities.exceptions.exceptionfactory import ExceptionFactory
from src.utilities.schemahandler import SchemaHandler

information_bp = Blueprint(name="information", import_name=__name__)
schema_handler = SchemaHandler()


@information_bp.route('/information/<string:property_id>', methods=['GET'])
def get_information(user_id: str, property_id: str):
    """Gets an individual property information."""

    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")
    data = property_information_collection.find_one({'property_id': property_id,
                                                     'user_id': user_id})
    logger.info(f"Data: {data}")
    if data == None:
        raise ExceptionFactory("Information not found").database_operation_failed() 

    data["_id"] = str(data["_id"])
    return {"success": True, "message": "information_data", "body": json.loads(json.dumps(data))}


@information_bp.route('/information', methods=['POST'])
def create_information(user_id: str):
    """Creates a property information."""

    response = user_info_collection.find_one({'user_id': user_id})
    logger.info(f"Response: {response}")
    if response == None:
        raise ExceptionFactory("").database_operation_failed()
    else:
        data = request.json
        data["user_id"] = user_id
        schema_handler.validate_property_info(data)
        response = property_information_collection.insert_one(data)
        return success("Property information created")


@information_bp.route('/information/<string:property_id>', methods=['PUT'])
def update_information(user_id: str, property_id: str):
    """Updates individual property information."""

    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")

    data = request.json
    query = {'user_id': user_id, 'property_id': property_id}
    response = property_information_collection.update_one(query, {'$set': data})

    if response.modified_count < 1:
        raise ExceptionFactory("").database_operation_failed()
        
    logger.info(f"Response: {response.matched_count}")
    return success("information data updated")
    


@information_bp.route('/information/<string:property_id>', methods=['DELETE'])
def delete_information(user_id: str, property_id: str):
    """Deletes a property information."""
    
    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")
    
    response = property_information_collection.delete_one({'user_id': user_id,
                                            'property_id': property_id})
    if response.deleted_count < 1:
        raise ExceptionFactory("").database_operation_failed()

    return success("information data deleted")
        
