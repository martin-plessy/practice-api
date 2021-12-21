from flask.testing import FlaskClient
from pytest import mark
from tests.utils import assert_bad_request, assert_conflict, assert_no_content, assert_not_found, assert_json, assert_not_found
from typing import Any, Dict

# GET /employee-type
# -----------------------------------------------------------------------------

def test_get(client: FlaskClient):
    assert_json(client.get('/employee-type/'), 200, [])

# GET /employee-type/<int:id>
# -----------------------------------------------------------------------------

def test_get_id_nonint(client: FlaskClient):
    # Returns 404 thanks to Flask's typed URL dynamic sections.
    assert_not_found(client.get('/employee-type/frog'))

def test_get_id_404(client: FlaskClient):
    assert_not_found(client.get('/employee-type/404'))

# POST /employee-type
# -----------------------------------------------------------------------------

@mark.parametrize(('input', 'expected_validation_messages'), [(
    { 'type': 42 },
    { 'type': 'Not a valid string.' }
), (
    { 'type': '' },
    { 'type': 'Length must be between 1 and 50.' }
), (
    { 'type': None },
    { 'type': 'Field may not be null.' }
), (
    { },
    { 'type': 'Missing data for required field.' }
), (
    { 'type': '-------10|-------20|-------30|-------40|-------50| TOO LONG' },
    { 'type': 'Length must be between 1 and 50.' }
)])
def test_post_invalid(client: FlaskClient, input: Dict[str, Any], expected_validation_messages: Dict[str, Any]):
    assert_bad_request(client.post('/employee-type/', json = input), expected_validation_messages)

def test_post_duplicate(client: FlaskClient):
    assert_json(client.post('/employee-type/', json = {
        'type': 'Duplicate'
    }), 201, {
        'uid': 1,
        'type': 'Duplicate'
    })

    assert_conflict(client.post('/employee-type/', json = {
        'type': 'Duplicate'
    }), {
        'type': 'Value must be unique.'
    })

def test_post_rejects_uid(client: FlaskClient):
    assert_bad_request(client.post('/employee-type/', json = {
        'uid': 42,
        'type': '42'
    }), {
        'uid': 'Unknown field.'
    })

def test_post(client: FlaskClient):
    assert_json(client.post('/employee-type/', json = {
        'type': 'A'
    }), 201, {
        'uid': 1,
        'type': 'A'
    })

    assert_json(client.get('/employee-type/'), 200, [
        { 'uid': 1, 'type': 'A' }
    ])

    assert_json(client.get('/employee-type/1'), 200, {
        'uid': 1,
        'type': 'A'
    })

    assert_json(client.post('/employee-type/', json = {
        'type': 'B'
    }), 201, {
        'uid': 2,
        'type': 'B'
    })

    assert_json(client.get('/employee-type/'), 200, [
        { 'uid': 1, 'type': 'A' },
        { 'uid': 2, 'type': 'B' }
    ])

    assert_json(client.get('/employee-type/1'), 200, {
        'uid': 1,
        'type': 'A'
    })

    assert_json(client.get('/employee-type/2'), 200, {
        'uid': 2,
        'type': 'B'
    })

# PUT /employee-type/<int:id>
# -----------------------------------------------------------------------------

def test_put_id_nonint(client: FlaskClient):
    # Returns 404 thanks to Flask's typed URL dynamic sections.
    assert_not_found(client.put('/employee-type/frog', json = {
        'type': 'X'
    }))

def test_put_id_404(client: FlaskClient):
    assert_not_found(client.put('/employee-type/404', json = {
        'type': 'X'
    }))

@mark.parametrize(('input', 'expected_validation_messages'), [(
    { 'type': 42 },
    { 'type': 'Not a valid string.' }
), (
    { 'type': '' },
    { 'type': 'Length must be between 1 and 50.' }
), (
    { 'type': None },
    { 'type': 'Field may not be null.' }
), (
    { },
    { 'type': 'Missing data for required field.' }
), (
    { 'type': '-------10|-------20|-------30|-------40|-------50| TOO LONG' },
    { 'type': 'Length must be between 1 and 50.' }
)])
def test_put_invalid(client: FlaskClient, input: Dict[str, Any], expected_validation_messages: Dict[str, Any]):
    client.post('/employee-type/', json = {
        'type': 'A'
    })

    assert_bad_request(client.put('/employee-type/1', json = input), expected_validation_messages)

def test_put_duplicate(client: FlaskClient):
    client.post('/employee-type/', json = { 'type': 'Duplicate' })
    client.post('/employee-type/', json = { 'type': 'B' })

    assert_conflict(client.put('/employee-type/2', json = {
        'type': 'Duplicate'
    }), {
        'type': 'Value must be unique.'
    })

def test_put_accepts_self_duplicate(client: FlaskClient):
    client.post('/employee-type/', json = { 'type': 'Solo' })

    assert_json(client.put('/employee-type/1', json = {
        'type': 'Solo'
    }), 200, {
        'uid': 1,
        'type': 'Solo'
    })

def test_put_rejects_uid_changes(client: FlaskClient):
    client.post('/employee-type/', json = { 'type': 'A' })

    assert_bad_request(client.put('/employee-type/1', json = {
        'uid': 42,
        'type': 'X'
    }), {
        'uid': 'Unknown field.'
    })

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
    assert_not_found(client.delete('/employee-type/frog'))

def test_delete_id_404(client: FlaskClient):
    # Idempotent.
    assert_no_content(client.delete('/employee-type/404'))

def test_delete(client: FlaskClient):
    client.post('/employee-type/', json = { 'type': 'A' })
    client.post('/employee-type/', json = { 'type': 'B' })

    assert_json(client.get('/employee-type/'), 200, [
        { 'uid': 1, 'type': 'A' },
        { 'uid': 2, 'type': 'B' }
    ])

    assert_no_content(client.delete('/employee-type/1'))
    assert_json(client.get('/employee-type/'), 200, [
        { 'uid': 2, 'type': 'B' }
    ])
    assert_not_found(client.get('/employee-type/1'))
