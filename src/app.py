from flask import Flask

# load modules
from endpoints.user import user_bp
from endpoints.property import property_bp
from endpoints.information import information_bp

# init Flask app
app = Flask(__name__)

# register blueprints. ensure that all paths are versioned!
app.register_blueprint(user_bp, url_prefix="/")
app.register_blueprint(property_bp, url_prefix="/user/<string:user_id>")
app.register_blueprint(information_bp, url_prefix="/user/<string:user_id>")

if __name__ == '__main__':
    app.run()
