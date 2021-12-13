from sqlite3 import Connection, connect, PARSE_DECLTYPES, Row
from flask import current_app, Flask, g

def init_app_db(app: Flask):
    app.teardown_appcontext(close_db)

def open_db() -> Connection:
    if 'db' not in g:
        g.db = connect(current_app.config['DATABASE'], detect_types = PARSE_DECLTYPES)
        g.db.row_factory = Row

    return g.db

def close_db(_ = None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def create_db():
    db = open_db()

    for sql_file_path in [
        '../data/employee_type.create.sql',
        # '../data/employee.create.sql',
        # '../data/practice.create.sql',
        # '../data/_fk.create.sql',
    ]:
        with current_app.open_resource(sql_file_path) as sql_file:
            db.executescript(sql_file.read().decode('utf8'))

def fill_db():
    db = open_db()

    for sql_file_path in [
        '../data/employee_type.insert.sql',
        # '../data/employee.insert.sql',
        # '../data/practice.insert.sql',
    ]:
        with current_app.open_resource(sql_file_path) as sql_file:
            db.executescript(sql_file.read().decode('utf8'))
