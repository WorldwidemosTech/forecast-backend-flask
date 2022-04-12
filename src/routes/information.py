from flask import Blueprint, request
from src.config.logger import logger

information_bp = Blueprint(name="information", import_name=__name__)


@information_bp.route('/information/<string:property_id>', methods=['GET'])
def get_information(user_id: str, property_id: str):
    """Gets an individual property information."""
    print("UserId: ", user_id)
    print("PropertyId: ", property_id)
    return {"success": True, "message": "information_data"}


@information_bp.route('/information', methods=['POST'])
def create_information(user_id: str):
    """Creates a property information."""
    logger.info("UserId: %s", user_id)
    print("UserId: ", user_id)
    data = request.json
    return {"success": True, "message": "information_data"}


@information_bp.route('/information/<string:property_id>', methods=['PUT'])
def update_information(user_id: str, property_id: str):
    """Updates individual property information."""
    print("UserId: ", user_id)
    print("PropertyId: ", property_id)
    data = request.json
    return {"success": True, "message": "information_data"}


@information_bp.route('/information/<string:property_id>', methods=['DELETE'])
def delete_information(user_id: str, property_id: str):
    """Deletes a property information."""
    print("UserId: ", user_id)
    print("PropertyId: ", property_id)
    return {"success": True, "message": "information_data"}
