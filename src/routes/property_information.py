from flask import Blueprint, request
from config.logger import logger
from db_config import property_information
import json

information_bp = Blueprint(name="information", import_name=__name__)


@information_bp.route('/information/<string:property_id>', methods=['GET'])
def get_information(user_id: str, property_id: str):
    """Gets an individual property information."""
    try:
        logger.info(f"UserId: {user_id}")
        logger.info(f"PropertyId: {property_id}")
        data = property_information.find_one({'property_id': property_id,
                                    'user_id': user_id})
       
        data["_id"] = str(data["_id"])
           

        return {"success": True, "message": "information_data", "body": json.loads(data)}

    except Exception as e:
        logger.error(e)
        return {"success": False, "message": "Error getting information data"}


@information_bp.route('/information', methods=['POST'])
def create_information(user_id: str):
    """Creates a property information."""
    try:
    
        logger.info(f"UserId: {user_id}")
        data = request.json
        data["user_id"] = user_id
        property_information.insert_one(data)
        return {"success": True, "message": "information_data"}
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"success": False, "message": "information_data"}


@information_bp.route('/information/<string:property_id>', methods=['PUT'])
def update_information(user_id: str, property_id: str):
    """Updates individual property information."""
    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")
    try:
        data = request.json
        logger.info(f"Payload: {data}")
        property_information.update_one({'user_id': user_id, 
                                        'property_id': property_id}, {'$set': data})
        return {"success": True, "message": "information_data"}

    except Exception as e:
        logger.error(f"Error: {e}")
        return {"success": False, "message": "information_data"}


@information_bp.route('/information/<string:property_id>', methods=['DELETE'])
def delete_information(user_id: str, property_id: str):
    """Deletes a property information."""
    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")
    try:
        property_information.delete_one({'user_id': user_id, 
                                        'property_id': property_id})
        return {"success": True, "message": "information_data"}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"success": False, "message": "information_data"}
