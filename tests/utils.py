from typing import Any, Dict, List, Union
from werkzeug import test

def assert_json(response: test.TestResponse, expected_code: int, expected_body: Union[List, Dict[str, Any], None] = None):
    assert response.status_code == expected_code

    if expected_code == 204:
        assert response.data == b''
    elif expected_code == 404:
        pass
    else:
        assert response.mimetype == 'application/json'
        assert response.json == expected_body
