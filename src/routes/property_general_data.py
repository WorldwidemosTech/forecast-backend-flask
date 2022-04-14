from flask import Blueprint, request
from src.config.logger import logger
from src.utilities.schemahandler import SchemaHandler

property_bp = Blueprint(name="property", import_name=__name__)
schema_handler = SchemaHandler()


@property_bp.route('/property/<string:property_id>', methods=['GET'])
def get_property(user_id: str, property_id: str):
    """Gets an individual property general data."""
    print("UserId: ", user_id)
    print("PropertyId: ", property_id)
    return {"success": True, "message": "property_data"}


@property_bp.route('/property', methods=['GET'])
def get_property_list(user_id: str):
    """Gets a list of properties general data associated to user."""
    print("UserId: ", user_id)
    return {"success": True, "message": "property_list"}


@property_bp.route('/property', methods=['POST'])
def create_property(user_id: str):
    """Creates a property general data."""
    print("UserId: ", user_id)
    data = request.json
    schema_handler.validate_property_data(request.json)
    return {"success": True, "message": "property_data"}


@property_bp.route('/property/<string:property_id>', methods=['PUT'])
def update_property(user_id: str, property_id: str):
    """Updates individual property general data."""
    print("UserId: ", user_id)
    print("PropertyId: ", property_id)
    data = request.json
    return {"success": True, "message": "property_data"}


@property_bp.route('/property/<string:property_id>', methods=['DELETE'])
def delete_property(user_id: str, property_id: str):
    """Deletes a property general data."""
    print("UserId: ", user_id)
    print("PropertyId: ", property_id)
    return {"success": True, "message": "property_data"}
