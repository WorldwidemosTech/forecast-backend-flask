from flask import Blueprint, request

scenario_bp = Blueprint(name="scenario", import_name=__name__)


@scenario_bp.route('/scenario/<string:scenario_id>', methods=['GET'])
def get_scenario(user_id: str, property_id: str):
    """Gets an individual property scenario."""
    print("UserId: ", user_id)
    print("PropertyId: ", property_id)
    return {"success": True, "message": "scenario_data"}

@scenario_bp.route('/property/<string:property_id>/scenario', methods=['GET'])
def get_scenario_list(user_id: str, property_id: str):
    """Gets an individual property scenario."""
    print("UserId: ", user_id)
    print("PropertyId: ", property_id)
    return {"success": True, "message": "scenario_data_list"}


@scenario_bp.route('/scenario', methods=['POST'])
def create_scenario(user_id: str):
    """Creates a property scenario."""
    print("UserId: ", user_id)
    data = request.json
    return {"success": True, "message": "scenario_data"}


@scenario_bp.route('/scenario/<string:scenario_id>', methods=['PUT'])
def update_scenario(user_id: str, property_id: str):
    """Updates individual property scenario."""
    print("UserId: ", user_id)
    print("PropertyId: ", property_id)
    data = request.json
    return {"success": True, "message": "scenario_data"}


@scenario_bp.route('/scenario/<string:scenario_id>', methods=['DELETE'])
def delete_scenario(user_id: str, property_id: str):
    """Deletes a property scenario."""
    print("UserId: ", user_id)
    print("PropertyId: ", property_id)
    return {"success": True, "message": "scenario_data"}
