from flask.json import jsonify
from app.cli import init_app_cli
from app.db import init_app_db
from app.employee_type import blueprint as employee_type
from flask import Flask
from os import makedirs, path
from typing import Any, Mapping

def create_app(test_config: Mapping[str, Any] = None):
    app = Flask(__name__, instance_relative_config = True)

    app.config.from_mapping(
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.from_mapping(test_config)

    makedirs(app.instance_path, exist_ok = True)

    init_app_db(app)
    init_app_cli(app)
    init_app_routes(app)

    return app

def init_app_routes(app: Flask):
    app.register_blueprint(employee_type, url_prefix = '/employee-type')

    @app.errorhandler(404)
    def handle_404(_):
        return jsonify({ 'title': 'not found' }), 404
