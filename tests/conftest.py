from flask.app import Flask
from flask.testing import FlaskClient
from app import create_app
from app.db import create_db
from os import close, unlink
from pytest import fixture
from tempfile import mkstemp
from tests.utils import Given, Then, When

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
def client(app: Flask):
    return app.test_client()

@fixture
def given(client: FlaskClient):
    return Given(client)

@fixture
def when(client: FlaskClient):
    return When(client)

@fixture
def then(when: When):
    return Then(when)
