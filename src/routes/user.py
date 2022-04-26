from flask import Blueprint, request

from src.utilities.schemahandler import SchemaHandler
from src.utilities.respond import success
from src.db_config import user
from src.utilities.exceptions.exceptionfactory import ExceptionFactory
import json
from src.config.logger import logger

user_bp = Blueprint(name="user", import_name=__name__)
schema_handler = SchemaHandler()


@user_bp.route('/user/<string:user_id>', methods=['GET'])
def get_user(user_id: str):
    """Gets an individual user data."""
    response = user.find_one({'user_id': user_id})
    response['_id'] = str(response["_id"])
    if response == None:
        raise ExceptionFactory("Information not found").invalid_dict_parameter_value()
    return {"success": True, "message": "information_data", "body": json.loads(json.dumps(response))}


@user_bp.route('/user', methods=['POST'])
def create_user():
    """Creates a user."""
    data = request.json
    schema_handler.validate_user(data)
    response = user.insert_one(data)

    if response.inserted_id == None:
        raise ExceptionFactory("User not created").invalid_dict_parameter_value()
    logger.info(str(response.inserted_id))
    return success(f"User created successfully with id: {str(response.inserted_id)}")


@user_bp.route('/user/<string:user_id>', methods=['PUT'])
def update_user(user_id: str):
    """Updates individual user data."""
    data = request.json
    schema_handler.validate_user(data)
    response = user.update_one({'user_id': user_id}, {'$set': data})
    if response.modified_count < 1:
        raise ExceptionFactory("").database_operation_failed()
    return success("User updated successfully")


@user_bp.route('/user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id: str):
    """Deletes a user data."""
    logger.info(f"UserId: {user_id}")
    
    response = user.delete_one({'user_id': user_id})
    if response.deleted_count < 1:
        raise ExceptionFactory("").database_operation_failed()
        
    return success("information data deleted")
