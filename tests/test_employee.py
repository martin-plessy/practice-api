from tests.utils import Given, Then, When

# GET /employees
# -----------------------------------------------------------------------------

def test_get(given: Given, when: When, then: Then):
    when.get_all_employees()
    then.ok_200()
    then.json([
    ])

# GET /employees/<int:id>
# -----------------------------------------------------------------------------

def test_get_id_nonint(given: Given, when: When, then: Then):
    when.get_employee('frog')
    then.not_found_404()

def test_get_id_404(given: Given, when: When, then: Then):
    when.get_employee('404')
    then.not_found_404()

# POST /employees
# -----------------------------------------------------------------------------

def test_post_invalid_1(given: Given, when: When, then: Then):
    when.post_employee({
        'name': 42,
        'email': 42,
        'telephone': 42,
        'employee_type_uid': 'frog'
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Not a valid string.',
        'email': 'Not a valid string.',
        'telephone': 'Not a valid string.',
        'employee_type_uid': 'Not a valid integer.'
    })

def test_post_invalid_2(given: Given, when: When, then: Then):
    when.post_employee({
        'name': '',
        'email': '',
        'telephone': '',
        'employee_type_uid': 404
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Length must be between 1 and 70.',
        'email': 'Length must be between 1 and 255.',
        'telephone': 'Length must be between 1 and 32.',
        'employee_type_uid': 'Not referencing an existing resource.'
    })

def test_post_invalid_3(given: Given, when: When, then: Then):
    when.post_employee({
        'name': None,
        'email': None,
        'telephone': None,
        'employee_type_uid': None
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Field may not be null.',
        'email': 'Field may not be null.',
        'telephone': 'Field may not be null.',
        'employee_type_uid': 'Field may not be null.'
    })

def test_post_invalid_4(given: Given, when: When, then: Then):
    when.post_employee({
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Missing data for required field.',
        'email': 'Missing data for required field.',
        'telephone': 'Missing data for required field.',
        'employee_type_uid': 'Missing data for required field.'
    })

def test_post_invalid_5(given: Given, when: When, then: Then):
    when.post_employee({
        'name': 'X' * 71,
        'email': 'X' * 256,
        'telephone': 'X' * 33,
        'employee_type_uid': 404
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Length must be between 1 and 70.',
        'email': 'Length must be between 1 and 255.',
        'telephone': 'Length must be between 1 and 32.',
        'employee_type_uid': 'Not referencing an existing resource.'
    })

def test_post_invalid_uid_extra(given: Given, when: When, then: Then):
    when.post_employee({
        'uid': 42,
        'name': 'A',
        'email': 'a@unit.test',
        'telephone': '07 999 000001',
        'employee_type_uid': 404
    })
    then.bad_request_400()
    then.validation_messages({
        'uid': 'Unknown field.',
        'employee_type_uid': 'Not referencing an existing resource.'
    })

def test_post_invalid_employee_type_extra(given: Given, when: When, then: Then):
    when.post_employee({
        'name': 'A',
        'email': 'a@unit.test',
        'telephone': '07 999 000001',
        'employee_type': {
            'type': 'T'
        }
    })
    then.bad_request_400()
    then.validation_messages({
        'employee_type': 'Unknown field.'
    })

def test_post(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()

    when.post_employee({
        'name': 'A',
        'email': 'a@unit.test',
        'telephone': '07 999 000001',
        'employee_type_uid': employee_type['uid']
    })
    then.created_201()
    then.json({
        'uid': 1,
        'name': 'A',
        'email': 'a@unit.test',
        'telephone': '07 999 000001',
        'employee_type': employee_type
    })

def test_post_get_multiple(given: Given, when: When, then: Then):
    first_type = given.an_employee_type()
    second_type = given.an_employee_type()

    first = given.an_employee(of_type = first_type['uid'])
    second = given.an_employee(of_type = second_type['uid'])

    when.get_all_employees()
    then.ok_200()
    then.json([
        first,
        second
    ])

    when.get_employee(first['uid'])
    then.ok_200()
    then.json(first)

    when.get_employee(second['uid'])
    then.ok_200()
    then.json(second)

# PUT /employees/<int:id>
# -----------------------------------------------------------------------------

def test_put_id_nonint(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()

    when.put_employee('frog', {
        'name': 'A',
        'email': 'a@unit.test',
        'telephone': '07 999 000001',
        'employee_type_uid': employee_type['uid']
    })
    then.not_found_404()

def test_put_id_404(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()

    when.put_employee('404', {
        'name': 'A',
        'email': 'a@unit.test',
        'telephone': '07 999 000001',
        'employee_type_uid': employee_type['uid']
    })
    then.not_found_404()

def test_put_invalid_1(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()
    employee = given.an_employee(of_type = employee_type['uid'])

    when.put_employee(employee['uid'], {
        'name': 42,
        'email': 42,
        'telephone': 42,
        'employee_type_uid': 'frog'
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Not a valid string.',
        'email': 'Not a valid string.',
        'telephone': 'Not a valid string.',
        'employee_type_uid': 'Not a valid integer.'
    })

def test_put_invalid_2(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()
    employee = given.an_employee(of_type = employee_type['uid'])

    when.put_employee(employee['uid'], {
        'name': '',
        'email': '',
        'telephone': '',
        'employee_type_uid': 404
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Length must be between 1 and 70.',
        'email': 'Length must be between 1 and 255.',
        'telephone': 'Length must be between 1 and 32.',
        'employee_type_uid': 'Not referencing an existing resource.'
    })

def test_put_invalid_3(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()
    employee = given.an_employee(of_type = employee_type['uid'])

    when.put_employee(employee['uid'], {
        'name': None,
        'email': None,
        'telephone': None,
        'employee_type_uid': None
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Field may not be null.',
        'email': 'Field may not be null.',
        'telephone': 'Field may not be null.',
        'employee_type_uid': 'Field may not be null.'
    })

def test_put_invalid_4(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()
    employee = given.an_employee(of_type = employee_type['uid'])

    when.put_employee(employee['uid'], {
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Missing data for required field.',
        'email': 'Missing data for required field.',
        'telephone': 'Missing data for required field.',
        'employee_type_uid': 'Missing data for required field.'
    })

def test_put_invalid_5(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()
    employee = given.an_employee(of_type = employee_type['uid'])

    when.put_employee(employee['uid'], {
        'name': 'X' * 71,
        'email': 'X' * 256,
        'telephone': 'X' * 33,
        'employee_type_uid': 404
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Length must be between 1 and 70.',
        'email': 'Length must be between 1 and 255.',
        'telephone': 'Length must be between 1 and 32.',
        'employee_type_uid': 'Not referencing an existing resource.'
    })

def test_put_invalid_employee_type_extra(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()
    employee = given.an_employee(of_type = employee_type['uid'])

    when.put_employee(employee['uid'], {
        'name': 'A',
        'email': 'a@unit.test',
        'telephone': '07 999 000001',
        'employee_type': {
            'type': 'T'
        }
    })
    then.bad_request_400()
    then.validation_messages({
        'employee_type': 'Unknown field.'
    })

def test_put_invalid_uid_extra(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()
    employee = given.an_employee(of_type = employee_type['uid'])

    when.put_employee(employee['uid'], {
        'uid': 42,
        'name': 'A',
        'email': 'a@unit.test',
        'telephone': '07 999 000001',
        'employee_type': {
            'type': 'T'
        }
    })
    then.bad_request_400()
    then.validation_messages({
        'uid': 'Unknown field.'
    })

def test_put(given: Given, when: When, then: Then):
    first_type = given.an_employee_type()
    second_type = given.an_employee_type()

    employee = given.an_employee(of_type = first_type['uid'])

    when.put_employee(employee['uid'], {
        'name': 'A',
        'email': 'a@unit.test',
        'telephone': '07 999 000001',
        'employee_type_uid': second_type['uid']
    })
    then.ok_200()
    then.json({
        'uid': employee['uid'],
        'name': 'A',
        'email': 'a@unit.test',
        'telephone': '07 999 000001',
        'employee_type': second_type
    })

def test_put_get_multiple(given: Given, when: When, then: Then):
    first_type = given.an_employee_type()
    second_type = given.an_employee_type()

    first_employee = given.an_employee(of_type = first_type['uid'])
    second_employee = given.an_employee(of_type = second_type['uid'])

    when.put_employee(second_employee['uid'], {
        'name': 'A',
        'email': 'a@unit.test',
        'telephone': '07 999 000001',
        'employee_type_uid': first_type['uid']
    })

    when.get_employee(second_employee['uid'])
    then.ok_200()
    then.json({
        'uid': second_employee['uid'],
        'name': 'A',
        'email': 'a@unit.test',
        'telephone': '07 999 000001',
        'employee_type': first_type
    })

    when.get_all_employees()
    then.ok_200()
    then.json([
        first_employee,
        {
           'uid': second_employee['uid'],
            'name': 'A',
            'email': 'a@unit.test',
            'telephone': '07 999 000001',
            'employee_type': first_type
        }
    ])

# DELETE /employees/<int:id>
# -----------------------------------------------------------------------------

def test_delete_id_nonint(given: Given, when: When, then: Then):
    when.delete_employee('frog')
    then.not_found_404()

def test_delete_id_404(given: Given, when: When, then: Then):
    when.delete_employee('404')
    then.no_content_204() # Idempotent!

def test_delete(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()

    first_employee = given.an_employee(of_type = employee_type['uid'])
    second_employee = given.an_employee(of_type = employee_type['uid'])

    when.get_all_employees()
    then.ok_200()
    then.json([
        first_employee,
        second_employee
    ])

    when.delete_employee(first_employee['uid'])
    then.no_content_204()

    when.get_all_employees()
    then.ok_200()
    then.json([
        second_employee
    ])

    when.get_employee(first_employee['uid'])
    then.not_found_404()
