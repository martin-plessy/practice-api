from flask.testing import FlaskClient
from typing import Any, Dict, Optional, Tuple
from werkzeug import test

class Given:
    def __init__(self, client: FlaskClient) -> None:
        self._client = client
        self._employee_type_counter = 0
        self._employee_counter = 0
        self._practice_counter = 0

    def an_employee_type(self) -> Dict[str, Any]:
        """
        Creates a new employee type, with no employee attached.
        """

        self._employee_type_counter = self._employee_type_counter + 1

        response = self._client.post('/employee-types/', json = {
            'type': f'Employee Type #{ self._employee_type_counter }'
        })

        return response.json

    def an_employee(self, of_type: Optional[Any] = None, in_practice: Optional[Any] = None) -> Dict[str, Any]:
        """
        Creates a new employee type, with no employee attached.

        | Parameter     | Value  | Description
        | ------------- | ------ | --------------------------------------------
        | `of_type`     | A UID  | The employee type's UID of the new employee.
        | `of_type`     | `None` | Creates a new employee type on the fly.
        | `in_practice` | A UID  | The practice's UID of the new employee.
        | `in_practice` | `None` | Creates a new practice on the fly.
        """

        if of_type is None:
            of_type = self.an_employee_type()['uid']

        if in_practice is None:
            in_practice = self.a_practice()['uid']

        self._employee_counter = self._employee_counter + 1

        response = self._client.post('/employees/', json = {
            'name': f'Employee #{ self._employee_counter }',
            'email': f'employee-n{ self._employee_counter }@unit.test',
            'telephone': f'07 123 { self._employee_counter :06}',
            'employee_type_uid': of_type,
            'practice_uid': in_practice
        })

        return response.json

    def a_practice(self) -> Dict[str, Any]:
        """
        Creates a new practice, with no manager, and no employee attached.
        """

        self._practice_counter = self._practice_counter + 1

        response = self._client.post('/practices/', json = {
            'name': f'Practice #{ self._practice_counter }',
            'address': f'{ self._practice_counter } Test Street, Exeter',
            'telephone': f'07 234 { self._practice_counter :06}'
        })

        return response.json

    def a_practice_with_a_manager(self, of_type: Optional[Any] = None) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Creates a new practice and a new employee,
        attaches the employee as the practice's sole employee and manager.

        | Parameter     | Value  | Description
        | ------------- | ------ | --------------------------------------------
        | `of_type`     | A UID  | The employee type's UID of the new manager.
        | `of_type`     | `None` | Creates a new employee type on the fly.
        """

        manager = self.an_employee(of_type = of_type)
        practice = manager['practice']

        manager_uid = manager['uid']
        practice_uid = practice['uid']
        self._client.put(f'/practices/{ practice_uid }/manager/{ manager_uid }')

        practice['manager'] = manager.copy()
        del practice['manager']['practice']

        return practice, manager

class When:
    def __init__(self, client: FlaskClient) -> None:
        self._client = client
        self._last_response: Optional[test.TestResponse] = None

    def __call__(self, response: test.TestResponse) -> None:
        self._last_response = response

    # Employee Types
    # -------------------------------------------------------------------------

    def get_all_employee_types(self):
        self._last_response = self._client.get('/employee-types/')

    def post_employee_type(self, json: Dict[str, Any]):
        self._last_response = self._client.post('/employee-types/', json = json)

    def get_employee_type(self, uid: Any):
        self._last_response = self._client.get(f'/employee-types/{ uid }')

    def put_employee_type(self, uid: Any, json: Dict[str, Any]):
        self._last_response = self._client.put(f'/employee-types/{ uid }', json = json)

    def delete_employee_type(self, uid: Any):
        self._last_response = self._client.delete(f'/employee-types/{ uid }')

    # Employees
    # -------------------------------------------------------------------------

    def get_all_employees(self):
        self._last_response = self._client.get('/employees/')

    def post_employee(self, json: Dict[str, Any]):
        self._last_response = self._client.post('/employees/', json = json)

    def get_employee(self, uid: Any):
        self._last_response = self._client.get(f'/employees/{ uid }')

    def put_employee(self, uid: Any, json: Dict[str, Any]):
        self._last_response = self._client.put(f'/employees/{ uid }', json = json)

    def delete_employee(self, uid: Any):
        self._last_response = self._client.delete(f'/employees/{ uid }')

    # Practices
    # -------------------------------------------------------------------------

    def get_all_practices(self):
        self._last_response = self._client.get('/practices/')

    def post_practice(self, json: Dict[str, Any]):
        self._last_response = self._client.post('/practices/', json = json)

    def get_practice(self, uid: Any):
        self._last_response = self._client.get(f'/practices/{ uid }')

    def put_practice(self, uid: Any, json: Dict[str, Any]):
        self._last_response = self._client.put(f'/practices/{ uid }', json = json)

    def delete_practice(self, uid: Any):
        self._last_response = self._client.delete(f'/practices/{ uid }')

    # Practice Managers
    # -------------------------------------------------------------------------

    def put_practice_manager(self, practice_uid: Any, manager_uid: Any):
        self._last_response = self._client.put(f'/practices/{ practice_uid }/manager/{ manager_uid }')

    def delete_practice_manager(self, practice_uid: Any):
        self._last_response = self._client.delete(f'/practices/{ practice_uid }/manager/')

class Then:
    def __init__(self, when: When) -> None:
        self._when = when

    def __call__(self) -> Optional[test.TestResponse]:
        return self._when._last_response

    def json(self, expected_json: Dict[str, Any]):
        self._assert_mimetype('application/json')
        self._assert_json(expected_json)

    def error_message(self, expected_message: str):
        self._assert_mimetype('application/json')
        self._assert_json(expected_message, self._when._last_response.json['message'], 'error message')

    def validation_messages(self, expected_validation_messages):
        self._assert_mimetype('application/json')

        for field, message in expected_validation_messages.items():
            self._assert_json([ message ], self._when._last_response.json['errors']['json'][field], f'validation message for \'{ field }\'')

    def _assert_mimetype(self, expected_mimetype: int):
        if self._when._last_response.mimetype != expected_mimetype:
            raise AssertionError(f'Expected mimetype { expected_mimetype }, where actual was { self._when._last_response.mimetype }.')

    def _assert_json(self, expected_json: Any, actual_json: Optional[Any] = None, label: str = 'json'):
        if actual_json is None:
            actual_json = self._when._last_response.json

        if actual_json != expected_json:
            raise AssertionError(f'Expected { label } { expected_json }, where actual was { actual_json }.')

    # Status Codes
    # -------------------------------------------------------------------------

    def _assert_status_code(self, expected_code: int):
        if self._when._last_response.status_code != expected_code:
            raise AssertionError(f'Expected status code { expected_code }, where actual was { self._when._last_response.status_code }.')

    def ok_200(self):
        self._assert_status_code(200)

    def created_201(self):
        self._assert_status_code(201)

    def accepted_202(self):
        self._assert_status_code(202)

    def non_authoritative_information_203(self):
        self._assert_status_code(203)

    def no_content_204(self):
        self._assert_status_code(204)
        assert self._when._last_response.data == b''

    def reset_content_205(self):
        self._assert_status_code(205)

    def partial_content_206(self):
        self._assert_status_code(206)

    def multi_status_207(self):
        self._assert_status_code(207)

    def already_reported_208(self):
        self._assert_status_code(208)

    def im_used_226(self):
        self._assert_status_code(226)

    def multiple_choices_300(self):
        self._assert_status_code(300)

    def moved_permanently_301(self):
        self._assert_status_code(301)

    def found_302(self):
        self._assert_status_code(302)

    def see_other_303(self):
        self._assert_status_code(303)

    def not_modified_304(self):
        self._assert_status_code(304)

    def use_proxy_305(self):
        self._assert_status_code(305)

    def temporary_redirect_307(self):
        self._assert_status_code(307)

    def permanent_redirect_308(self):
        self._assert_status_code(308)

    def bad_request_400(self):
        self._assert_status_code(400)

    def unauthorized_401(self):
        self._assert_status_code(401)

    def payment_required_402(self):
        self._assert_status_code(402)

    def forbidden_403(self):
        self._assert_status_code(403)

    def not_found_404(self):
        self._assert_status_code(404)

    def method_not_allowed_405(self):
        self._assert_status_code(405)

    def not_acceptable_406(self):
        self._assert_status_code(406)

    def proxy_authentication_required_407(self):
        self._assert_status_code(407)

    def request_timeout_408(self):
        self._assert_status_code(408)

    def conflict_409(self):
        self._assert_status_code(409)

    def gone_410(self):
        self._assert_status_code(410)

    def length_required_411(self):
        self._assert_status_code(411)

    def precondition_failed_412(self):
        self._assert_status_code(412)

    def request_entity_too_large_413(self):
        self._assert_status_code(413)

    def request_uri_too_long_414(self):
        self._assert_status_code(414)

    def unsupported_media_type_415(self):
        self._assert_status_code(415)

    def requested_range_not_satisfiable_416(self):
        self._assert_status_code(416)

    def expectation_failed_417(self):
        self._assert_status_code(417)

    def enhance_your_calm_420(self):
        self._assert_status_code(420)

    def unprocessable_entity_422(self):
        self._assert_status_code(422)

    def locked_423(self):
        self._assert_status_code(423)

    def failed_dependency_424(self):
        self._assert_status_code(424)

    def upgrade_required_426(self):
        self._assert_status_code(426)

    def precondition_required_428(self):
        self._assert_status_code(428)

    def too_many_requests_429(self):
        self._assert_status_code(429)

    def request_header_fields_too_large_431(self):
        self._assert_status_code(431)

    def unavailable_for_legal_reasons_451(self):
        self._assert_status_code(451)
