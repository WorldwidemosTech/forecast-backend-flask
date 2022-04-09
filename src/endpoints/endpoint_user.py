from flask import Blueprint, jsonify, request

# define the blueprint
endpoint_user = Blueprint(name="endpoint_user_test", import_name=__name__)

# note: global variables can be accessed from view functions
x = 5

# add view function to the blueprint
@endpoint_user.route('/test', methods=['GET'])
def test():
    output = {"msg": "I'm the test endpoint from endpoint_user."}
    return jsonify(output)

# add view function to the blueprint
@endpoint_user.route('/plus', methods=['POST'])
def plus_x():
    # retrieve body data from input JSON
    data = request.get_json()
    in_val = data['number']
    # compute result and output as JSON
    result = in_val + x
    output = {"msg": f"Your result is: '{result}'"}
    return jsonify(output)