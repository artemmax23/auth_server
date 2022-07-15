import os
from datetime import timedelta

import humanfriendly as hf
from flask import Flask

from controllers.main import jwt
from .main_bp import main_bp


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=
                                                       hf.parse_timespan(os.getenv('ACCESS_LIFETIME', '30m')))
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(seconds=
                                                        hf.parse_timespan(os.getenv('REFRESH_LIFETIME', '7d')))

    app.register_blueprint(main_bp)

    jwt.init_app(app)

    app.app_context().push()

    return app
