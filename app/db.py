from flask import current_app, Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app_db(app: Flask):
    db.init_app(app)

def create_db():
    db.create_all()

def fill_db():
    for sql_file_path in [
        '../data/employee_type.insert.sql',
        # '../data/employee.insert.sql',
        # '../data/practice.insert.sql',
    ]:
        with current_app.open_resource(sql_file_path) as sql_file:
            db.engine.execute(sql_file.read().decode('utf8'))
