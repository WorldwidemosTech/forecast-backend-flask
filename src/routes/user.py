from flask import Blueprint, request
import json

from src.config.database import user_info_collection
from src.utilities.exceptions.exceptionfactory import ExceptionFactory
from src.utilities.respond import success
from src.utilities.schemahandler import SchemaHandler

user_bp = Blueprint(name="user", import_name=__name__)
schema_handler = SchemaHandler()


@user_bp.route('/user/<string:user_id>', methods=['GET'])
def get_user(user_id: str):
    """Gets an individual user data."""
    response = user_info_collection.find_one({"user_id": user_id})
    if not response:
        raise ExceptionFactory("").resource_not_found()
    response["_id"] = str(response["_id"])
    return success(response)


@user_bp.route('/user', methods=['POST'])
def create_user():
    """Creates a user."""
    schema_handler.validate_user(request.json)

    response = user_info_collection.insert_one(request.json)
    if not response.acknowledged:
        raise ExceptionFactory("").database_operation_failed()
    return success({"inserted_id": str(response.inserted_id)})


@user_bp.route('/user/<string:user_id>', methods=['PUT'])
def update_user(user_id: str):
    """Updates individual user data."""
    schema_handler.validate_user(request.json)
    response = user_info_collection.update_one({"user_id": user_id}, {"$set": request.json})
    if not response.acknowledged:
        raise ExceptionFactory("").database_operation_failed()
    return success({"modified_count": response.modified_count})


@user_bp.route('/user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id: str):
    """Deletes a user data."""
    response = user_info_collection.delete_one({"user_id": user_id})
    if not response.acknowledged:
        raise ExceptionFactory("").database_operation_failed()
    return success({"deleted_count": response.deleted_count})