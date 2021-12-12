from flask.testing import FlaskClient

def test_index(client: FlaskClient):
    response = client.get('/')

    assert response.status_code == 200
    assert response.mimetype == 'application/json'
    assert response.json == {
        'message': 'Hello, there!'
    }
