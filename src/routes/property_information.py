import json

from flask import Blueprint, request
from bson import ObjectId
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
        raise ExceptionFactory("").database_operation_failed() 

    data["_id"] = str(data["_id"])
    return success({"body": json.loads(json.dumps(data))})


@information_bp.route('/information/<string:property_id>', methods=['POST'])
def create_information(user_id: str, property_id: str):
    """Creates a property information."""

    response = user_info_collection.find_one({'user_id': user_id})
    logger.info(f"Response: {response}")
    data = request.json
    #schema_handler.validate_property_info(data)
    response2 = property_information_collection.update_one({
                                                    "property_id": ObjectId(property_id),
                                                    "user_id":user_id},
                                                    {"$push":data})

    if response == None:
        raise ExceptionFactory("").database_operation_failed()
    
    return success({"modified_count": str(response2.modified_count)}) 


@information_bp.route('/information/<string:property_id>', methods=['PUT'])
def update_information(user_id: str, property_id: str):
    """Updates individual property information."""

    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")

    data = request.json
    schema_handler.validate_property_info(data)
    query = {'user_id': user_id, 'property_id': property_id}
    response = property_information_collection.update_one(query, {'$set': data})

    if response.modified_count < 1:
        raise ExceptionFactory("").database_operation_failed()
        
    logger.info(f"Response: {response.matched_count}")
    return success({"modified_count": str(response.modified_count)})
    


@information_bp.route('/information/<string:property_id>', methods=['DELETE'])
def delete_information(user_id: str, property_id: str):
    """Deletes a property information."""
    
    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")
    
    response = property_information_collection.delete_one({'user_id': user_id,
                                            'property_id': property_id})
    if response.deleted_count < 1:
        raise ExceptionFactory("").database_operation_failed()

    return success({"deleted_count": str(response.deleted_count)})
        
