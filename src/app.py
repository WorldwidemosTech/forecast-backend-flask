from flask import Flask, jsonify
import sys

# load modules
from src.endpoints.endpoint_user import endpoint_user


# init Flask app
app = Flask(__name__)

# register blueprints. ensure that all paths are versioned!
app.register_blueprint(endpoint_user, url_prefix="/api/v1/path_for_blueprint_x")
