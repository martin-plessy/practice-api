from app.db import create_db, fill_db
from click import command
from flask.cli import with_appcontext

def init_app_cli(app):
    app.cli.add_command(_create_db)
    app.cli.add_command(_fill_db)

@command('create-db')
@with_appcontext
def _create_db():
    create_db()

@command('fill-db')
@with_appcontext
def _fill_db():
    fill_db()
