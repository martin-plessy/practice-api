from typing import Any, Dict, List, Optional, Union
from werkzeug import test

def assert_json(response: test.TestResponse, expected_code: int, expected_body: Union[List, Dict[str, Any], None] = None):
    assert response.status_code == expected_code
    assert response.mimetype == 'application/json'
    assert response.json == expected_body

def assert_no_content(response: test.TestResponse):
    assert response.status_code == 204
    assert response.data == b''

def assert_bad_request(response: test.TestResponse, expected_validation_messages: Optional[Dict[str, str]] = None):
    _assert_err(response, 400, 'Bad Request', expected_validation_messages)

def assert_conflict(response: test.TestResponse, expected_validation_messages: Optional[Dict[str, str]] = None):
    _assert_err(response, 409, 'Conflict', expected_validation_messages)

def assert_not_found(response: test.TestResponse):
    assert response.status_code == 404

def _assert_err(response: test.TestResponse, expected_code: int, expected_status: str, expected_validation_messages: Optional[Dict[str, str]] = None):
    assert response.status_code == expected_code
    assert response.mimetype == 'application/json'

    assert response.json['code'] == expected_code
    assert response.json['status'] == expected_status

    for field, message in expected_validation_messages.items():
        assert response.json['errors']['json'][field] == [ message ]
