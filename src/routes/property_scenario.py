from flask import Blueprint, request
from src.config.logger import logger
from src.config.database import user_info_collection, property_general_data_collection
from src.config.database import property_scenarios_collection
from src.utilities.exceptions.exceptionfactory import ExceptionFactory
from src.utilities.schemahandler import SchemaHandler
from src.utilities.respond import success
from bson.objectid import ObjectId
import json

scenario_bp = Blueprint(name="scenario", import_name=__name__)
schema_handler = SchemaHandler()

@scenario_bp.route('/scenario/<string:scenario_id>', methods=['GET'])
def get_scenario(user_id: str, property_id: str):
    """Gets an individual property scenario."""

    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")
    data = property_scenarios_collection.find_one({'property_id': property_id,
                                                     'user_id': user_id})
    logger.info(f"Data: {data}")
    if data == None:
        raise ExceptionFactory("").database_operation_failed() 

    data["_id"] = str(data["_id"])
    return success({"body": json.loads(json.dumps(data))})

@scenario_bp.route('/property/<string:property_id>/scenario', methods=['GET'])
def get_scenario_list(user_id: str, property_id: str):
    """Gets an individual property scenario."""
    logger.info(f"Getting property scenarios for user: {user_id}.")

    response = property_scenarios_collection.find({"user_id": user_id})
    response = list(response)

    if not response:
        raise ExceptionFactory("").resource_not_found()

    scenarios = []
    for item in response:
        item["_id"] = str(item["_id"])
        scenarios.append(item)

    return success(scenarios)


@scenario_bp.route('/scenario', methods=['POST'])
def create_scenario(user_id: str):
    """Creates a property scenario."""
    data = request.json
    property_id = data["property_id"]
    response = property_general_data_collection.find_one({'_id': ObjectId(property_id)})
    logger.info(f"Response: {response}")
    if response == None:
        raise ExceptionFactory("").database_operation_failed()
    
    
    data["user_id"] = user_id
    schema_handler.validate_property_scenario(data)
    response = property_scenarios_collection.insert_one(data)
    return success({"inserted_id": str(response.inserted_id)})


@scenario_bp.route('/scenario/<string:scenario_id>', methods=['PUT'])
def update_scenario(user_id: str, property_id: str):
    """Updates individual property scenario."""
    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")

    data = request.json
    schema_handler.validate_property_scenario(data)
    query = {'user_id': user_id, 'property_id': property_id}
    response = property_scenarios_collection.update_one(query, {'$set': data})

    if response.modified_count < 1:
        raise ExceptionFactory("").database_operation_failed()
        
    logger.info(f"Response: {response.matched_count}")
    return success({"modified_count": str(response.modified_count)})


@scenario_bp.route('/scenario/<string:scenario_id>', methods=['DELETE'])
def delete_scenario(user_id: str, property_id: str):
    """Deletes a property scenario."""
    logger.info(f"UserId: {user_id}")
    logger.info(f"PropertyId: {property_id}")
    
    response = property_scenarios_collection.delete_one({'user_id': user_id,
                                            'property_id': property_id})
    if response.deleted_count < 1:
        raise ExceptionFactory("").database_operation_failed()

    return success({"deleted_count": str(response.deleted_count)})
