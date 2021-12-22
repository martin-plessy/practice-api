from flask.testing import FlaskClient
from tests.utils import assert_bad_request, assert_conflict, assert_no_content, assert_not_found, assert_json, assert_not_found

# GET /employees
# -----------------------------------------------------------------------------

def test_get(client: FlaskClient):
    assert_json(
        client.get('/employees/'),
        expected_code = 200,
        expected_body = [
        ])

# GET /employees/<int:id>
# -----------------------------------------------------------------------------

def test_get_id_nonint(client: FlaskClient):
    assert_not_found(
        client.get('/employees/frog'))

def test_get_id_404(client: FlaskClient):
    assert_not_found(
        client.get('/employees/404'))

# POST /employees
# -----------------------------------------------------------------------------

def test_post_invalid(client: FlaskClient):
    assert_bad_request(
        client.post('/employees/', json = {
            'name': 42,
            'email': 42,
            'telephone': 42
        }),
        expected_validation_messages = {
            'name': 'Not a valid string.',
            'email': 'Not a valid string.',
            'telephone': 'Not a valid string.'
        })

    assert_bad_request(
        client.post('/employees/', json = {
            'name': '',
            'email': '',
            'telephone': ''
        }),
        expected_validation_messages = {
            'name': 'Length must be between 1 and 70.',
            'email': 'Length must be between 1 and 255.',
            'telephone': 'Length must be between 1 and 32.'
        })

    assert_bad_request(
        client.post('/employees/', json = {
            'name': None,
            'email': None,
            'telephone': None
        }),
        expected_validation_messages = {
            'name': 'Field may not be null.',
            'email': 'Field may not be null.',
            'telephone': 'Field may not be null.'
        })

    assert_bad_request(
        client.post('/employees/', json = {
        }),
        expected_validation_messages = {
            'name': 'Missing data for required field.',
            'email': 'Missing data for required field.',
            'telephone': 'Missing data for required field.'
        })

    assert_bad_request(
        client.post('/employees/', json = {
            'name': 'X' * 71,
            'email': 'X' * 256,
            'telephone': 'X' * 33
        }),
        expected_validation_messages = {
            'name': 'Length must be between 1 and 70.',
            'email': 'Length must be between 1 and 255.',
            'telephone': 'Length must be between 1 and 32.'
        })

def test_post_rejects_uid(client: FlaskClient):
    assert_bad_request(
        client.post('/employees/', json = {
            'uid': 42,
            'name': '42',
            'email': '42@universe.com',
            'telephone': '07666 420042'
        }),
        expected_validation_messages  ={
            'uid': 'Unknown field.'
        })

def test_post(client: FlaskClient):
    assert_json(
        client.post('/employees/', json = {
            'name': 'A',
            'email': 'a@ali.com',
            'telephone': '07 123 123456'
        }),
        expected_code = 201,
        expected_body = {
            'uid': 1,
            'name': 'A',
            'email': 'a@ali.com',
            'telephone': '07 123 123456'
        })

    assert_json(
        client.get('/employees/'),
        expected_code = 200,
        expected_body = [
            { 'uid': 1, 'name': 'A', 'email': 'a@ali.com', 'telephone': '07 123 123456' }
        ])

    assert_json(
        client.get('/employees/1'),
        expected_code = 200,
        expected_body = {
            'uid': 1,
            'name': 'A',
            'email': 'a@ali.com',
            'telephone': '07 123 123456'
        })

    assert_json(
        client.post('/employees/', json = {
            'name': 'B',
            'email': 'b@baba.com',
            'telephone': '07 123 123456'
        }),
        expected_code = 201,
        expected_body = {
            'uid': 2,
            'name': 'B',
            'email': 'b@baba.com',
            'telephone': '07 123 123456'
        })

    assert_json(
        client.get('/employees/'),
        expected_code = 200,
        expected_body = [
            { 'uid': 1, 'name': 'A', 'email': 'a@ali.com', 'telephone': '07 123 123456' },
            { 'uid': 2, 'name': 'B', 'email': 'b@baba.com', 'telephone': '07 123 123456' }
        ])

    assert_json(
        client.get('/employees/1'),
        expected_code = 200,
        expected_body = {
            'uid': 1,
            'name': 'A',
            'email': 'a@ali.com',
            'telephone': '07 123 123456'
        })

    assert_json(
        client.get('/employees/2'),
        expected_code = 200,
        expected_body = {
            'uid': 2,
            'name': 'B',
            'email': 'b@baba.com',
            'telephone': '07 123 123456'
        })

# PUT /employees/<int:id>
# -----------------------------------------------------------------------------

def test_put_id_nonint(client: FlaskClient):
    assert_not_found(
        client.put('/employees/frog', json = {
            'name': 'X',
            'email': 'x@x.com',
            'telephone': '07 123 123456'
        }))

def test_put_id_404(client: FlaskClient):
    assert_not_found(
        client.put('/employees/404', json = {
            'name': 'X',
            'email': 'x@x.com',
            'telephone': '07 123 123456'
        }))


def test_put_invalid(client: FlaskClient):
    client.post('/employees/', json = {
        'name': 'A',
        'email': 'a@ali.com',
        'telephone': '07 123 123456'
    })

    assert_bad_request(
        client.put('/employees/1', json = {
            'name': 42,
            'email': 42,
            'telephone': 42
        }),
        expected_validation_messages = {
            'name': 'Not a valid string.',
            'email': 'Not a valid string.',
            'telephone': 'Not a valid string.'
        })

    assert_bad_request(
        client.put('/employees/1', json = {
            'name': '',
            'email': '',
            'telephone': ''
        }),
        expected_validation_messages = {
            'name': 'Length must be between 1 and 70.',
            'email': 'Length must be between 1 and 255.',
            'telephone': 'Length must be between 1 and 32.'
        })

    assert_bad_request(
        client.put('/employees/1', json = {
            'name': None,
            'email': None,
            'telephone': None
        }),
        expected_validation_messages = {
            'name': 'Field may not be null.',
            'email': 'Field may not be null.',
            'telephone': 'Field may not be null.'
        })

    assert_bad_request(
        client.put('/employees/1', json = {
        }),
        expected_validation_messages = {
            'name': 'Missing data for required field.',
            'email': 'Missing data for required field.',
            'telephone': 'Missing data for required field.'
        })

    assert_bad_request(
        client.put('/employees/1', json = {
            'name': 'X' * 71,
            'email': 'X' * 256,
            'telephone': 'X' * 33
        }),
        expected_validation_messages = {
            'name': 'Length must be between 1 and 70.',
            'email': 'Length must be between 1 and 255.',
            'telephone': 'Length must be between 1 and 32.'
        })

def test_put_rejects_uid_changes(client: FlaskClient):
    client.post('/employees/', json = {
        'name': 'A',
        'email': 'a@ali.com',
        'telephone': '07 123 123456'
    })

    assert_bad_request(
        client.put('/employees/1', json = {
            'uid': 42,
            'name': 'A',
            'email': 'a@ali.com',
            'telephone': '07 123 123456'
        }),
        expected_validation_messages = {
            'uid': 'Unknown field.'
        })

def test_put(client: FlaskClient):
    client.post('/employees/', json = {
        'name': 'A',
        'email': 'a@ali.com',
        'telephone': '07 123 123456'
    })

    client.post('/employees/', json = {
        'name': 'B',
        'email': 'b@baba.com',
        'telephone': '07 123 123456'
    })

    assert_json(
        client.put('/employees/1', json = {
            'name': 'X',
            'email': 'x@tatic.com',
            'telephone': '07 123 123456'
        }),
        expected_code = 200,
        expected_body = {
            'uid': 1,
            'name': 'X',
            'email': 'x@tatic.com',
            'telephone': '07 123 123456'
        })

    assert_json(
        client.get('/employees/'),
        expected_code = 200,
        expected_body = [
            { 'uid': 1, 'name': 'X', 'email': 'x@tatic.com', 'telephone': '07 123 123456' },
            { 'uid': 2, 'name': 'B', 'email': 'b@baba.com', 'telephone': '07 123 123456' }
        ])

    assert_json(
        client.get('/employees/1'),
        expected_code = 200,
        expected_body = {
            'uid': 1,
            'name': 'X',
            'email': 'x@tatic.com',
            'telephone': '07 123 123456'
        })

    assert_json(
        client.put('/employees/2', json = {
            'name': 'Y',
            'email': 'y@oming.com',
            'telephone': '07 123 123456'
        }),
        expected_code = 200,
        expected_body = {
            'uid': 2,
            'name': 'Y',
            'email': 'y@oming.com',
            'telephone': '07 123 123456'
        })

    assert_json(
        client.get('/employees/'),
        expected_code = 200,
        expected_body = [
            { 'uid': 1, 'name': 'X', 'email': 'x@tatic.com', 'telephone': '07 123 123456' },
            { 'uid': 2, 'name': 'Y', 'email': 'y@oming.com', 'telephone': '07 123 123456' }
        ])

    assert_json(
        client.get('/employees/1'),
        expected_code = 200,
        expected_body = {
            'uid': 1,
            'name': 'X',
            'email': 'x@tatic.com',
            'telephone': '07 123 123456'
        })

    assert_json(
        client.get('/employees/2'),
        expected_code = 200,
        expected_body = {
            'uid': 2,
            'name': 'Y',
            'email': 'y@oming.com',
            'telephone': '07 123 123456'
        })

# DELETE /employees/<int:id>
# -----------------------------------------------------------------------------

def test_delete_id_nonint(client: FlaskClient):
    assert_not_found(
        client.delete('/employees/frog'))

def test_delete_id_404(client: FlaskClient):
    # Idempotent.
    assert_no_content(
        client.delete('/employees/404'))

def test_delete(client: FlaskClient):
    client.post('/employees/', json = {
        'name': 'A',
        'email': 'a@ali.com',
        'telephone': '07 123 123456'
    })

    client.post('/employees/', json = {
        'name': 'B',
        'email': 'b@baba.com',
        'telephone': '07 123 123456'
    })

    assert_json(
        client.get('/employees/'),
        expected_code = 200,
        expected_body = [
            { 'uid': 1, 'name': 'A', 'email': 'a@ali.com', 'telephone': '07 123 123456' },
            { 'uid': 2, 'name': 'B', 'email': 'b@baba.com', 'telephone': '07 123 123456' }
        ])

    assert_no_content(
        client.delete('/employees/1'))

    assert_json(
        client.get('/employees/'),
        expected_code = 200,
        expected_body = [
            { 'uid': 2, 'name': 'B', 'email': 'b@baba.com', 'telephone': '07 123 123456' }
        ])

    assert_not_found(
        client.get('/employees/1'))
