from app.cli import init_app_cli
from app.db import init_app_db
from app.employee_type import bp as employee_type_bp
from flask import Flask
from flask_smorest import Api
from os import makedirs, path
from typing import Any, Mapping

def create_app(test_config: Mapping[str, Any] = None):
    app = Flask(__name__, instance_relative_config = True)

    app.config.from_mapping(
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(app.instance_path, 'app.sqlite'),
        API_TITLE = 'Practice API',
        API_VERSION = 'v1',
        OPENAPI_VERSION = '3.0.2',
        OPENAPI_URL_PREFIX = '/',
        OPENAPI_SWAGGER_UI_PATH = '/',
        OPENAPI_SWAGGER_UI_URL = 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.24.2/'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.from_mapping(test_config)

    makedirs(app.instance_path, exist_ok = True)

    api = Api(app)

    init_app_db(app)
    init_app_cli(app)
    init_api_resources(api)

    return app

def init_api_resources(api: Api):
    api.register_blueprint(employee_type_bp)
