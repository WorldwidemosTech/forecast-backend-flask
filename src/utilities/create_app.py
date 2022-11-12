import traceback

from flask import Flask
from flask_cors import CORS

from src.routes.property_general_data import property_bp
from src.routes.property_information import information_bp
from src.routes.property_scenario import scenario_bp
from src.routes.property_forecast import property_forecast_bp
from src.routes.user import user_bp
from src.utilities.exceptions.exception import APIException
from src.utilities.logging_ import get_logger
from src.utilities.respond import error


def handle_api_exception(e):
    # Logger for the class that raised the error
    logger = get_logger(__name__)
    logger.error(traceback.format_exc())

    return error(e.error, e.description, e.http_code, e.field, e.failed_field_value)


def create_app():
    app = Flask(__name__)

    # Load app error handlers
    app.register_error_handler(APIException, handle_api_exception)

    # Blueprints
    app.register_blueprint(user_bp, url_prefix="/")
    app.register_blueprint(property_bp, url_prefix="/user/<string:user_id>")
    app.register_blueprint(information_bp, url_prefix="/user/<string:user_id>")
    app.register_blueprint(scenario_bp, url_prefix="/user/<string:user_id>")
    app.register_blueprint(property_forecast_bp, url_prefix="/user/<string:user_id>")

    CORS(app)
    cors = CORS(app, resources={r"/user/*": {"origins": "*"}})
    return app
