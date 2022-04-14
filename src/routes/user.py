from flask import Blueprint, request
from src.config.logger import logger
from src.utilities.schemahandler import SchemaHandler

user_bp = Blueprint(name="user", import_name=__name__)
schema_handler = SchemaHandler()


@user_bp.route('/user/<string:user_id>', methods=['GET'])
def get_user(user_id: str):
    """Gets an individual user data."""
    return {"success": True, "message": "user_data"}


@user_bp.route('/user', methods=['POST'])
def create_user():
    """Creates a user."""
    schema_handler.validate_user(request.json)
    return {"success": True, "message": "user_data"}


@user_bp.route('/user/<string:user_id>', methods=['PUT'])
def update_user(user_id: str):
    """Updates individual user data."""
    return {"success": True, "message": "user_data"}


@user_bp.route('/user/<string:user_id>', methods=['DELETE'])
def delete_user(user_id: str):
    """Deletes a user data."""
    return {"success": True, "message": "user_data"}
