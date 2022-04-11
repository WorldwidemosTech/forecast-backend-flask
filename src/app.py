from flask import Flask

# load modules
from routes.user import user_bp
from routes.property import property_bp
from routes.information import information_bp
from routes.scenario import scenario_bp

# init Flask app
app = Flask(__name__)

# register blueprints. ensure that all paths are versioned!
app.register_blueprint(user_bp, url_prefix="/")
app.register_blueprint(property_bp, url_prefix="/user/<string:user_id>")
app.register_blueprint(information_bp, url_prefix="/user/<string:user_id>")
app.register_blueprint(scenario_bp, url_prefix="/user/<string:user_id>")

if __name__ == '__main__':
    app.run()
