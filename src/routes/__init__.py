from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager

from .main_bp import main_bp


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = "super-secret"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)

    app.register_blueprint(main_bp)

    jwt = JWTManager(app)
    jwt.init_app(app)

    app.app_context().push()

    return app
