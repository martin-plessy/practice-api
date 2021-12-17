from app import create_app
from app.db import create_db
from os import close, unlink
from pytest import fixture
from tempfile import mkstemp

@fixture
def app():
    db_file, db_file_path = mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + db_file_path,
    })

    with app.app_context():
        create_db()

    yield app

    close(db_file)
    unlink(db_file_path)

@fixture
def client(app):
    return app.test_client()

@fixture
def runner(app):
    return app.test_cli_runner()
