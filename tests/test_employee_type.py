from tests.utils import Given, Then, When

# GET /employee-types
# -----------------------------------------------------------------------------

def test_get(given: Given, when: When, then: Then):
    when.get_all_employee_types()
    then.ok_200()
    then.json([
    ])

# GET /employee-types/<int:id>
# -----------------------------------------------------------------------------

def test_get_id_nonint(given: Given, when: When, then: Then):
    when.get_employee_type('frog')
    then.not_found_404()

def test_get_id_404(given: Given, when: When, then: Then):
    when.get_employee_type('404')
    then.not_found_404()

# POST /employee-types
# -----------------------------------------------------------------------------

def test_post_invalid_type_not_string(given: Given, when: When, then: Then):
    when.post_employee_type({
        'type': 42
    })
    then.bad_request_400()
    then.validation_messages({
        'type': 'Not a valid string.'
    })

def test_post_invalid_type_empty_string(given: Given, when: When, then: Then):
    when.post_employee_type({
        'type': ''
    })
    then.bad_request_400()
    then.validation_messages({
        'type': 'Length must be between 1 and 50.'
    })

def test_post_invalid_type_null_string(given: Given, when: When, then: Then):
    when.post_employee_type({
        'type': None
    })
    then.bad_request_400()
    then.validation_messages({
        'type': 'Field may not be null.'
    })

def test_post_invalid_type_missing(given: Given, when: When, then: Then):
    when.post_employee_type({
    })
    then.bad_request_400()
    then.validation_messages({
        'type': 'Missing data for required field.'
    })

def test_post_invalid_type_large_string(given: Given, when: When, then: Then):
    when.post_employee_type({
        'type': 'X' * 51
    })
    then.bad_request_400()
    then.validation_messages({
        'type': 'Length must be between 1 and 50.'
    })

def test_post_invalid_type_duplicate(given: Given, when: When, then: Then):
    existing = given.an_employee_type()

    when.post_employee_type({
        'type': existing['type']
    })
    then.conflict_409()
    then.validation_messages({
        'type': 'Value must be unique.'
    })

def test_post_invalid_uid_extra(given: Given, when: When, then: Then):
    when.post_employee_type({
        'uid': 42,
        'type': '42'
    })
    then.bad_request_400()
    then.validation_messages({
        'uid': 'Unknown field.'
    })

def test_post(given: Given, when: When, then: Then):
    when.post_employee_type({
        'type': 'A'
    })
    then.created_201()
    then.json({
        'uid': 1,
        'type': 'A'
    })

def test_post_get(given: Given, when: When, then: Then):
    created = given.an_employee_type()

    when.get_all_employee_types()
    then.ok_200()
    then.json([
        created
    ])

    when.get_employee_type(created['uid'])
    then.ok_200()
    then.json(created)

def test_post_get_multiple(given: Given, when: When, then: Then):
    first = given.an_employee_type()
    second = given.an_employee_type()

    when.get_all_employee_types()
    then.ok_200()
    then.json([
        first,
        second
    ])

    when.get_employee_type(first['uid'])
    then.ok_200()
    then.json(first)

    when.get_employee_type(second['uid'])
    then.ok_200()
    then.json(second)

# PUT /employee-types/<int:id>
# -----------------------------------------------------------------------------

def test_put_id_nonint(given: Given, when: When, then: Then):
    when.put_employee_type('frog', {
        'type': 'X'
    })
    then.not_found_404()

def test_put_id_404(given: Given, when: When, then: Then):
    when.put_employee_type('404', {
        'type': 'X'
    })
    then.not_found_404()

def test_put_invalid_type_not_string(given: Given, when: When, then: Then):
    existing = given.an_employee_type()

    when.put_employee_type(existing['uid'], {
        'type': 42
    })
    then.bad_request_400()
    then.validation_messages({
        'type': 'Not a valid string.'
    })

def test_put_invalid_type_empty_string(given: Given, when: When, then: Then):
    existing = given.an_employee_type()

    when.put_employee_type(existing['uid'], {
        'type': ''
    })
    then.bad_request_400()
    then.validation_messages({
        'type': 'Length must be between 1 and 50.'
    })

def test_put_invalid_type_null(given: Given, when: When, then: Then):
    existing = given.an_employee_type()

    when.put_employee_type(existing['uid'], {
        'type': None
    })
    then.bad_request_400()
    then.validation_messages({
        'type': 'Field may not be null.'
    })

def test_put_invalid_type_missing(given: Given, when: When, then: Then):
    existing = given.an_employee_type()

    when.put_employee_type(existing['uid'], {
    })
    then.bad_request_400()
    then.validation_messages({
        'type': 'Missing data for required field.'
    })

def test_put_invalid_type_large_string(given: Given, when: When, then: Then):
    existing = given.an_employee_type()

    when.put_employee_type(existing['uid'], {
        'type': 'X' * 51
    })
    then.bad_request_400()
    then.validation_messages({
        'type': 'Length must be between 1 and 50.'
    })

def test_put_invalid_type_duplicate(given: Given, when: When, then: Then):
    first = given.an_employee_type()
    second = given.an_employee_type()

    when.put_employee_type(second['uid'], {
        'type': first['type']
    })
    then.conflict_409()
    then.validation_messages({
        'type': 'Value must be unique.'
    })

def test_put_self_duplicate(given: Given, when: When, then: Then):
    existing = given.an_employee_type()

    when.put_employee_type(existing['uid'], {
        'type': existing['type']
    })
    then.ok_200()
    then.json(existing)

def test_put_invalid_uid_extra(given: Given, when: When, then: Then):
    existing = given.an_employee_type()

    when.put_employee_type(existing['uid'], {
        'uid': 42,
        'type': 'X'
    })
    then.bad_request_400()
    then.validation_messages({
        'uid': 'Unknown field.'
    })

def test_put(given: Given, when: When, then: Then):
    existing = given.an_employee_type()

    when.put_employee_type(existing['uid'], {
        'type': 'X'
    })
    then.ok_200()
    then.json({
        'uid': existing['uid'],
        'type': 'X'
    })

def test_put_get_multiple(given: Given, when: When, then: Then):
    first = given.an_employee_type()
    second = given.an_employee_type()

    when.put_employee_type(first['uid'], {
        'type': 'X'
    })

    when.put_employee_type(second['uid'], {
        'type': 'Y'
    })

    when.get_all_employee_types()
    then.ok_200()
    then.json([
        {
            'uid': first['uid'],
            'type': 'X'
        },
        {
            'uid': second['uid'],
            'type': 'Y'
        }
    ])

# DELETE /employee-types/<int:id>
# -----------------------------------------------------------------------------

def test_delete_id_nonint(given: Given, when: When, then: Then):
    when.delete_employee_type('frog')
    then.not_found_404()

def test_delete_id_404(given: Given, when: When, then: Then):
    when.delete_employee_type('404')
    then.no_content_204() # Idempotent!

def test_delete_invalid_employee_type_with_employees(given: Given, when: When, then: Then):
    t = given.an_employee_type()
    e = given.an_employee(of_type = t['uid'])

    when.delete_employee_type(t['uid'])
    then.conflict_409()
    then.error_message('Employee type still has attached employees.')

def test_delete(given: Given, when: When, then: Then):
    existing = given.an_employee_type()

    when.delete_employee(existing['uid'])
    then.no_content_204()

def test_delete_get_multiple(given: Given, when: When, then: Then):
    first = given.an_employee_type()
    second = given.an_employee_type()

    when.get_all_employee_types()
    then.ok_200()
    then.json([
        first,
        second
    ])

    when.delete_employee_type(first['uid'])
    then.no_content_204()

    when.get_all_employee_types()
    then.ok_200()
    then.json([
        second
    ])

    when.get_employee_type(first['uid'])
    then.not_found_404()
