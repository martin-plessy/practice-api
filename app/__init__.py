from flask import Flask, jsonify
from os import makedirs
from typing import Any, Mapping

def create_app(test_config: Mapping[str, Any] = None):
    app = Flask(__name__, instance_relative_config = True)

    app.config.from_mapping(
        SECRET_KEY = 'dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent = True)
    else:
        app.config.from_mapping(test_config)

    makedirs(app.instance_path, exist_ok = True)

    @app.route('/')
    def index():
        return jsonify(
            message = 'Hello, there!'
        )

    return app
