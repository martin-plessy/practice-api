from flask.testing import FlaskClient
from tests.utils import assert_bad_request, assert_conflict, assert_no_content, assert_not_found, assert_json, assert_not_found

# GET /employee-types
# -----------------------------------------------------------------------------

def test_get(client: FlaskClient):
    assert_json(
        client.get('/employee-types/'),
        expected_code = 200,
        expected_body = [
        ])

# GET /employee-types/<int:id>
# -----------------------------------------------------------------------------

def test_get_id_nonint(client: FlaskClient):
    assert_not_found(
        client.get('/employee-types/frog'))

def test_get_id_404(client: FlaskClient):
    assert_not_found(
        client.get('/employee-types/404'))

# POST /employee-types
# -----------------------------------------------------------------------------

def test_post_invalid(client: FlaskClient):
    assert_bad_request(
        client.post('/employee-types/', json = {
            'type': 42
        }),
        expected_validation_messages = {
            'type': 'Not a valid string.'
        })

    assert_bad_request(
        client.post('/employee-types/', json = {
            'type': ''
        }),
        expected_validation_messages = {
            'type': 'Length must be between 1 and 50.'
        })

    assert_bad_request(
        client.post('/employee-types/', json = {
            'type': None
        }),
        expected_validation_messages = {
            'type': 'Field may not be null.'
        })

    assert_bad_request(
        client.post('/employee-types/', json = {
        }),
        expected_validation_messages = {
            'type': 'Missing data for required field.'
        })

    assert_bad_request(
        client.post('/employee-types/', json = {
            'type': 'X' * 51
        }),
        expected_validation_messages = {
            'type': 'Length must be between 1 and 50.'
        })

def test_post_duplicate(client: FlaskClient):
    assert_json(
        client.post('/employee-types/', json = {
            'type': 'Duplicate'
        }),
        expected_code = 201,
        expected_body = {
            'uid': 1,
            'type': 'Duplicate'
        })

    assert_conflict(
        client.post('/employee-types/', json = {
            'type': 'Duplicate'
        }),
        expected_validation_messages = {
            'type': 'Value must be unique.'
        })

def test_post_rejects_uid(client: FlaskClient):
    assert_bad_request(
        client.post('/employee-types/', json = {
            'uid': 42,
            'type': '42'
        }),
        expected_validation_messages  ={
            'uid': 'Unknown field.'
        })

def test_post(client: FlaskClient):
    assert_json(
        client.post('/employee-types/', json = {
            'type': 'A'
        }),
        expected_code = 201,
        expected_body = {
            'uid': 1,
            'type': 'A'
        })

    assert_json(
        client.get('/employee-types/'),
        expected_code = 200,
        expected_body = [
            { 'uid': 1, 'type': 'A' }
        ])

    assert_json(
        client.get('/employee-types/1'),
        expected_code = 200,
        expected_body = {
            'uid': 1,
            'type': 'A'
        })

    assert_json(
        client.post('/employee-types/', json = {
            'type': 'B'
        }),
        expected_code = 201,
        expected_body = {
            'uid': 2,
            'type': 'B'
        })

    assert_json(
        client.get('/employee-types/'),
        expected_code = 200,
        expected_body = [
            { 'uid': 1, 'type': 'A' },
            { 'uid': 2, 'type': 'B' }
        ])

    assert_json(
        client.get('/employee-types/1'),
        expected_code = 200,
        expected_body = {
            'uid': 1,
            'type': 'A'
        })

    assert_json(
        client.get('/employee-types/2'),
        expected_code = 200,
        expected_body = {
            'uid': 2,
            'type': 'B'
        })

# PUT /employee-types/<int:id>
# -----------------------------------------------------------------------------

def test_put_id_nonint(client: FlaskClient):
    assert_not_found(
        client.put('/employee-types/frog', json = {
            'type': 'X'
        }))

def test_put_id_404(client: FlaskClient):
    assert_not_found(
        client.put('/employee-types/404', json = {
            'type': 'X'
        }))


def test_put_invalid(client: FlaskClient):
    client.post('/employee-types/', json = {
        'type': 'A'
    })

    assert_bad_request(
        client.put('/employee-types/1', json = {
            'type': 42
        }),
        expected_validation_messages = {
            'type': 'Not a valid string.'
        })

    assert_bad_request(
        client.put('/employee-types/1', json = {
            'type': ''
        }),
        expected_validation_messages = {
            'type': 'Length must be between 1 and 50.'
        })

    assert_bad_request(
        client.put('/employee-types/1', json = {
            'type': None
        }),
        expected_validation_messages = {
            'type': 'Field may not be null.'
        })

    assert_bad_request(
        client.put('/employee-types/1', json = {
        }),
        expected_validation_messages = {
            'type': 'Missing data for required field.'
        })

    assert_bad_request(
        client.put('/employee-types/1', json = {
            'type': 'X' * 51
        }),
        expected_validation_messages = {
            'type': 'Length must be between 1 and 50.'
        })

def test_put_duplicate(client: FlaskClient):
    client.post('/employee-types/', json = {
        'type': 'Duplicate'
    })

    client.post('/employee-types/', json = {
        'type': 'B'
    })

    assert_conflict(
        client.put('/employee-types/2', json = {
            'type': 'Duplicate'
        }),
        expected_validation_messages = {
            'type': 'Value must be unique.'
        })

def test_put_accepts_self_duplicate(client: FlaskClient):
    client.post('/employee-types/', json = {
        'type': 'Solo'
    })

    assert_json(
        client.put('/employee-types/1', json = {
            'type': 'Solo'
        }),
        expected_code = 200,
        expected_body = {
            'uid': 1,
            'type': 'Solo'
        })

def test_put_rejects_uid_changes(client: FlaskClient):
    client.post('/employee-types/', json = {
        'type': 'A'
    })

    assert_bad_request(
        client.put('/employee-types/1', json = {
            'uid': 42,
            'type': 'X'
        }),
        expected_validation_messages = {
            'uid': 'Unknown field.'
        })

def test_put(client: FlaskClient):
    client.post('/employee-types/', json = {
        'type': 'A'
    })

    client.post('/employee-types/', json = {
        'type': 'B'
    })

    assert_json(
        client.put('/employee-types/1', json = {
            'type': 'X'
        }),
        expected_code = 200,
        expected_body = {
            'uid': 1,
            'type': 'X'
        })

    assert_json(
        client.get('/employee-types/'),
        expected_code = 200,
        expected_body = [
            { 'uid': 1, 'type': 'X' },
            { 'uid': 2, 'type': 'B' }
        ])

    assert_json(
        client.get('/employee-types/1'),
        expected_code = 200,
        expected_body = {
            'uid': 1,
            'type': 'X'
        })

    assert_json(
        client.put('/employee-types/2', json = {
            'type': 'Y'
        }),
        expected_code = 200,
        expected_body = {
            'uid': 2,
            'type': 'Y'
        })

    assert_json(
        client.get('/employee-types/'),
        expected_code = 200,
        expected_body = [
            { 'uid': 1, 'type': 'X' },
            { 'uid': 2, 'type': 'Y' }
        ])

    assert_json(
        client.get('/employee-types/1'),
        expected_code = 200,
        expected_body = {
            'uid': 1,
            'type': 'X'
        })

    assert_json(
        client.get('/employee-types/2'),
        expected_code = 200,
        expected_body = {
            'uid': 2,
            'type': 'Y'
        })

# DELETE /employee-types/<int:id>
# -----------------------------------------------------------------------------

def test_delete_id_nonint(client: FlaskClient):
    assert_not_found(
        client.delete('/employee-types/frog'))

def test_delete_id_404(client: FlaskClient):
    # Idempotent.
    assert_no_content(
        client.delete('/employee-types/404'))

def test_delete_protects_employee_type_with_employees(client: FlaskClient):
    client.post('/employee-types/', json = {
        'type': 'T'
    })

    client.post('/employees/', json = {
        'name': 'N',
        'email': 'e@mail.com',
        'telephone': '07123 456789',
        'employee_type_uid': 1
    })

    assert_conflict(
        client.delete('/employee-types/1'),
        expected_message = 'Employee type still has attached employees.')

def test_delete(client: FlaskClient):
    client.post('/employee-types/', json = {
        'type': 'A'
    })

    client.post('/employee-types/', json = {
        'type': 'B'
    })

    assert_json(
        client.get('/employee-types/'),
        expected_code = 200,
        expected_body = [
            { 'uid': 1, 'type': 'A' },
            { 'uid': 2, 'type': 'B' }
        ])

    assert_no_content(
        client.delete('/employee-types/1'))

    assert_json(
        client.get('/employee-types/'),
        expected_code = 200,
        expected_body = [
            { 'uid': 2, 'type': 'B' }
        ])

    assert_not_found(
        client.get('/employee-types/1'))
