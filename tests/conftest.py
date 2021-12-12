from app import create_app
from pytest import fixture

@fixture
def app():
    app = create_app({
        'TESTING': True
    })

    yield app

@fixture
def client(app):
    return app.test_client()

@fixture
def runner(app):
    return app.test_cli_runner()
