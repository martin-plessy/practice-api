from flask.testing import FlaskClient
from pytest import mark
from typing import Any, Dict, List, Union
from werkzeug import test

def assert_json(response: test.TestResponse, expected_code: int, expected_body: Union[List, Dict[str, Any], None] = None):
    assert response.status_code == expected_code

    if expected_code == 204:
        assert response.data == b''
    else:
        assert response.mimetype == 'application/json'
        assert response.json == expected_body

# GET /employee-type
# -----------------------------------------------------------------------------

def test_get(client: FlaskClient):
    assert_json(client.get('/employee-type/'), 200, [])

# GET /employee-type/<int:id>
# -----------------------------------------------------------------------------

def test_get_id_nonint(client: FlaskClient):
    # Returns 404 thanks to Flask's typed URL dynamic sections.
    assert_json(client.get('/employee-type/frog'), 404, {
        'title': 'not found'
    })

def test_get_id_404(client: FlaskClient):
    assert_json(client.get('/employee-type/404'), 404, {
        'title': 'not found'
    })

# POST /employee-type
# -----------------------------------------------------------------------------

@mark.parametrize(('input', 'expected_reason'), [
    ({ 'type': 42 }, 'must be string'),
    ({ 'type': '' }, 'required'),
    ({ 'type': None }, 'required'),
    ({ }, 'required'),
    ({ 'type': '-------10|-------20|-------30|-------40|-------50| TOO LONG' }, 'max length exceeded'),
])
def test_post_invalid(client: FlaskClient, input: Dict[str, Any], expected_reason: str):
    assert_json(client.post('/employee-type/', json = input), 400, {
        'title': 'bad request',
        'invalid-params': [
            { 'name': 'type', 'reason': expected_reason }
        ]
    })

def test_post_duplicate(client: FlaskClient):
    assert_json(client.post('/employee-type/', json = { 'type': 'Duplicate' }), 201, { 'uid': 1, 'type': 'Duplicate' })
    assert_json(client.post('/employee-type/', json = { 'type': 'Duplicate' }), 409, {
        'title': 'conflict',
        'invalid-params': [
            { 'name': 'type', 'reason': 'duplicated' }
        ]
    })

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
    assert_json(client.put('/employee-type/frog', json = { 'type': 'X' }), 404, {
        'title': 'not found'
    })

def test_put_id_404(client: FlaskClient):
    assert_json(client.put('/employee-type/404', json = { 'type': 'X' }), 404, {
        'title': 'not found'
    })

@mark.parametrize(('input', 'expected_reason'), [
    ({ 'type': 42 }, 'must be string'),
    ({ 'type': '' }, 'required'),
    ({ 'type': None }, 'required'),
    ({ }, 'required'),
    ({ 'type': '-------10|-------20|-------30|-------40|-------50| TOO LONG' }, 'max length exceeded'),
])
def test_put_invalid(client: FlaskClient, input: Dict[str, Any], expected_reason: str):
    client.post('/employee-type/', json = { 'type': 'A' })

    assert_json(client.put('/employee-type/1', json = input), 400, {
        'title': 'bad request',
        'invalid-params': [
            { 'name': 'type', 'reason': expected_reason }
        ]
    })

def test_put_duplicate(client: FlaskClient):
    client.post('/employee-type/', json = { 'type': 'Duplicate' })
    client.post('/employee-type/', json = { 'type': 'B' })

    assert_json(client.put('/employee-type/2', json = { 'type': 'Duplicate' }), 409, {
        'title': 'conflict',
        'invalid-params': [
            { 'name': 'type', 'reason': 'duplicated' }
        ]
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
    assert_json(client.delete('/employee-type/frog'), 404, {
        'title': 'not found'
    })

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
    assert_json(client.get('/employee-type/1'), 404, {
        'title': 'not found'
    })
