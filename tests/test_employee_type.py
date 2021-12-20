from flask.testing import FlaskClient
from pytest import mark
from typing import Any, Dict
from utils import assert_json

# GET /employee-type
# -----------------------------------------------------------------------------

def test_get(client: FlaskClient):
    assert_json(client.get('/employee-type/'), 200, [])

# GET /employee-type/<int:id>
# -----------------------------------------------------------------------------

def test_get_id_nonint(client: FlaskClient):
    # Returns 404 thanks to Flask's typed URL dynamic sections.
    assert_json(client.get('/employee-type/frog'), 404)

def test_get_id_404(client: FlaskClient):
    assert_json(client.get('/employee-type/404'), 404)

# POST /employee-type
# -----------------------------------------------------------------------------

@mark.parametrize(('input', 'expected_reason'), [
    ({ 'type': 42 }, 'Not a valid string.'),
    ({ 'type': '' }, 'Length must be between 1 and 50.'),
    ({ 'type': None }, 'Field may not be null.'),
    ({ }, 'Missing data for required field.'),
    ({ 'type': '-------10|-------20|-------30|-------40|-------50| TOO LONG' }, 'Length must be between 1 and 50.'),
])
def test_post_invalid(client: FlaskClient, input: Dict[str, Any], expected_reason: str):
    assert_json(client.post('/employee-type/', json = input), 400, {
        'type': [ expected_reason ]
    })

def test_post_duplicate(client: FlaskClient):
    assert_json(client.post('/employee-type/', json = { 'type': 'Duplicate' }), 201, { 'uid': 1, 'type': 'Duplicate' })
    assert_json(client.post('/employee-type/', json = { 'type': 'Duplicate' }), 409, {
        'type': [ 'Value must be unique.' ]
    })

def test_post_ignores_uid(client: FlaskClient):
    assert_json(client.post('/employee-type/', json = { 'uid': 42, 'type': '42' }), 201, { 'uid': 1, 'type': '42' })

def test_post(client: FlaskClient):
    assert_json(client.post('/employee-type/', json = { 'type': 'A' }), 201, { 'uid': 1, 'type': 'A' })
    assert_json(client.get('/employee-type/'), 200, [
        { 'uid': 1, 'type': 'A' }
    ])
    assert_json(client.get('/employee-type/1'), 200, { 'uid': 1, 'type': 'A' })

    assert_json(client.post('/employee-type/', json = { 'type': 'B' }), 201, { 'uid': 2, 'type': 'B' })
    assert_json(client.get('/employee-type/'), 200, [
        { 'uid': 1, 'type': 'A' },
        { 'uid': 2, 'type': 'B' }
    ])
    assert_json(client.get('/employee-type/1'), 200, { 'uid': 1, 'type': 'A' })
    assert_json(client.get('/employee-type/2'), 200, { 'uid': 2, 'type': 'B' })

# PUT /employee-type/<int:id>
# -----------------------------------------------------------------------------

def test_put_id_nonint(client: FlaskClient):
    # Returns 404 thanks to Flask's typed URL dynamic sections.
    assert_json(client.put('/employee-type/frog', json = { 'type': 'X' }), 404)

def test_put_id_404(client: FlaskClient):
    assert_json(client.put('/employee-type/404', json = { 'type': 'X' }), 404)

@mark.parametrize(('input', 'expected_reason'), [
    ({ 'type': 42 }, 'Not a valid string.'),
    ({ 'type': '' }, 'Length must be between 1 and 50.'),
    ({ 'type': None }, 'Field may not be null.'),
    ({ }, 'Missing data for required field.'),
    ({ 'type': '-------10|-------20|-------30|-------40|-------50| TOO LONG' }, 'Length must be between 1 and 50.'),
])
def test_put_invalid(client: FlaskClient, input: Dict[str, Any], expected_reason: str):
    client.post('/employee-type/', json = { 'type': 'A' })

    assert_json(client.put('/employee-type/1', json = input), 400, {
        'type': [ expected_reason ]
    })

def test_put_duplicate(client: FlaskClient):
    client.post('/employee-type/', json = { 'type': 'Duplicate' })
    client.post('/employee-type/', json = { 'type': 'B' })

    assert_json(client.put('/employee-type/2', json = { 'type': 'Duplicate' }), 409, {
        'type': [ 'Value must be unique.' ]
    })

def test_put_accepts_self_duplicate(client: FlaskClient):
    client.post('/employee-type/', json = { 'type': 'Solo' })

    assert_json(client.put('/employee-type/1', json = { 'type': 'Solo' }), 200, { 'uid': 1, 'type': 'Solo' })

def test_put_ignores_uid_changes(client: FlaskClient):
    client.post('/employee-type/', json = { 'type': 'A' })

    assert_json(client.put('/employee-type/1', json = { 'uid': 42, 'type': 'X' }), 200, { 'uid': 1, 'type': 'X' })

def test_put(client: FlaskClient):
    client.post('/employee-type/', json = { 'type': 'A' })
    client.post('/employee-type/', json = { 'type': 'B' })

    assert_json(client.put('/employee-type/1', json = { 'type': 'X' }), 200, { 'uid': 1, 'type': 'X' })
    assert_json(client.get('/employee-type/'), 200, [
        { 'uid': 1, 'type': 'X' },
        { 'uid': 2, 'type': 'B' }
    ])
    assert_json(client.get('/employee-type/1'), 200, { 'uid': 1, 'type': 'X' })

    assert_json(client.put('/employee-type/2', json = { 'type': 'Y' }), 200, { 'uid': 2, 'type': 'Y' })
    assert_json(client.get('/employee-type/'), 200, [
        { 'uid': 1, 'type': 'X' },
        { 'uid': 2, 'type': 'Y' }
    ])
    assert_json(client.get('/employee-type/1'), 200, { 'uid': 1, 'type': 'X' })
    assert_json(client.get('/employee-type/2'), 200, { 'uid': 2, 'type': 'Y' })

# DELETE /employee-type/<int:id>
# -----------------------------------------------------------------------------

def test_delete_id_nonint(client: FlaskClient):
    # Returns 404 thanks to Flask's typed URL dynamic sections.
    assert_json(client.delete('/employee-type/frog'), 404)

def test_delete_id_404(client: FlaskClient):
    # Idempotent.
    assert_json(client.delete('/employee-type/404'), 204)

def test_delete(client: FlaskClient):
    client.post('/employee-type/', json = { 'type': 'A' })
    client.post('/employee-type/', json = { 'type': 'B' })

    assert_json(client.get('/employee-type/'), 200, [
        { 'uid': 1, 'type': 'A' },
        { 'uid': 2, 'type': 'B' }
    ])

    assert_json(client.delete('/employee-type/1'), 204)
    assert_json(client.get('/employee-type/'), 200, [
        { 'uid': 2, 'type': 'B' }
    ])
    assert_json(client.get('/employee-type/1'), 404)
