from flask import current_app, Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow.exceptions import ValidationError
from marshmallow.types import Validator

db = SQLAlchemy()

def init_app_db(app: Flask):
    db.init_app(app)

def create_db():
    db.create_all()

def fill_db():
    for sql_file_path in [
        '../data/employee_type.insert.sql',
        '../data/employee.insert.sql',
        # '../data/practice.insert.sql',
    ]:
        with current_app.open_resource(sql_file_path) as sql_file:
            db.engine.execute(sql_file.read().decode('utf8'))

class FkReference(Validator):
    def __init__(self, model_class):
        self.model_class = model_class

    def __call__(self, value):
        if self.model_class.query.get(value) is None:
            raise ValidationError("Not referencing an existing resource.")

        return value
