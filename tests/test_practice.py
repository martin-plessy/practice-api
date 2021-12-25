from tests.utils import Given, Then, When

# GET /practices
# -----------------------------------------------------------------------------

def test_get(given: Given, when: When, then: Then):
    when.get_all_practices()
    then.ok_200()
    then.json([
    ])

# GET /practices/<int:id>
# -----------------------------------------------------------------------------

def test_get_id_nonint(given: Given, when: When, then: Then):
    when.get_practice('frog')
    then.not_found_404()

def test_get_id_404(given: Given, when: When, then: Then):
    when.get_practice('404')
    then.not_found_404()

# POST /practices
# -----------------------------------------------------------------------------

def test_post_invalid_1(given: Given, when: When, then: Then):
    when.post_practice({
        'name': 42,
        'address': 42,
        'telephone': 42,
        'manager_uid': 'frog'
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Not a valid string.',
        'address': 'Not a valid string.',
        'telephone': 'Not a valid string.',
        'manager_uid': 'Not a valid integer.'
    })

def test_post_invalid_2(given: Given, when: When, then: Then):
    when.post_practice({
        'name': '',
        'address': '',
        'telephone': '',
        'manager_uid': 404
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Length must be between 1 and 70.',
        'address': 'Length must be between 1 and 255.',
        'telephone': 'Length must be between 1 and 32.',
        'manager_uid': 'Not referencing an existing resource.'
    })

def test_post_invalid_3(given: Given, when: When, then: Then):
    when.post_practice({
        'name': None,
        'address': None,
        'telephone': None,
        'manager_uid': None
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Field may not be null.',
        'address': 'Field may not be null.',
        'telephone': 'Field may not be null.',
        # 'manager_uid' is optional.
    })

def test_post_invalid_4(given: Given, when: When, then: Then):
    when.post_practice({
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Missing data for required field.',
        'address': 'Missing data for required field.',
        'telephone': 'Missing data for required field.',
        # 'manager_uid' is optional.
    })

def test_post_invalid_5(given: Given, when: When, then: Then):
    when.post_practice({
        'name': 'X' * 71,
        'address': 'X' * 256,
        'telephone': 'X' * 33,
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Length must be between 1 and 70.',
        'address': 'Length must be between 1 and 255.',
        'telephone': 'Length must be between 1 and 32.',
        # 'manager_uid' is optional.
    })

def test_post_invalid_uid_extra(given: Given, when: When, then: Then):
    when.post_practice({
        'uid': 42,
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
    })
    then.bad_request_400()
    then.validation_messages({
        'uid': 'Unknown field.',
        # 'manager_uid' is optional.
    })

def test_post_invalid_manager_extra(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()

    when.post_practice({
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        'manager': {
            'name': 'A',
            'email': 'a@unit.test',
            'telephone': '07 999 000002',
            'manager_uid': employee_type['uid']
        }
    })
    then.bad_request_400()
    then.validation_messages({
        'manager': 'Unknown field.'
    })

def test_post_without_manager(given: Given, when: When, then: Then):
    when.post_practice({
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001'
    })
    then.created_201()
    then.json({
        'uid': 1,
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001'
    })

def test_post_with_manager(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()
    employee = given.an_employee(of_type = employee_type['uid'])

    when.post_practice({
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        'manager_uid': employee['uid']
    })
    then.created_201()
    then.json({
        'uid': 1,
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        'manager': employee
    })

def test_post_get_multiple(given: Given, when: When, then: Then):
    manager_type = given.an_employee_type()
    manager = given.an_employee(of_type = manager_type['uid'])

    first = given.a_practice()
    second = given.a_practice(with_manager = manager['uid'])

    when.get_all_practices()
    then.ok_200()
    then.json([
        first,
        second
    ])

    when.get_practice(first['uid'])
    then.ok_200()
    then.json(first)

    when.get_practice(second['uid'])
    then.ok_200()
    then.json(second)

# PUT /practices/<int:id>
# -----------------------------------------------------------------------------

def test_put_id_nonint(given: Given, when: When, then: Then):
    when.put_practice('frog', {
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001'
    })
    then.not_found_404()

def test_put_id_404(given: Given, when: When, then: Then):
    when.put_practice('404', {
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001'
    })
    then.not_found_404()

def test_put_invalid_1(given: Given, when: When, then: Then):
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
        'name': 42,
        'address': 42,
        'telephone': 42,
        'manager_uid': 'frog'
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Not a valid string.',
        'address': 'Not a valid string.',
        'telephone': 'Not a valid string.',
        'manager_uid': 'Not a valid integer.'
    })

def test_put_invalid_2(given: Given, when: When, then: Then):
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
        'name': '',
        'address': '',
        'telephone': '',
        'manager_uid': 404
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Length must be between 1 and 70.',
        'address': 'Length must be between 1 and 255.',
        'telephone': 'Length must be between 1 and 32.',
        'manager_uid': 'Not referencing an existing resource.'
    })

def test_put_invalid_3(given: Given, when: When, then: Then):
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
        'name': None,
        'address': None,
        'telephone': None,
        'manager_uid': None
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Field may not be null.',
        'address': 'Field may not be null.',
        'telephone': 'Field may not be null.',
        # 'manager_uid' is optional.
    })

def test_put_invalid_4(given: Given, when: When, then: Then):
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Missing data for required field.',
        'address': 'Missing data for required field.',
        'telephone': 'Missing data for required field.',
        # 'manager_uid' is optional.
    })

def test_put_invalid_5(given: Given, when: When, then: Then):
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
        'name': 'X' * 71,
        'address': 'X' * 256,
        'telephone': 'X' * 33
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Length must be between 1 and 70.',
        'address': 'Length must be between 1 and 255.',
        'telephone': 'Length must be between 1 and 32.',
        # 'manager_uid' is optional.
    })

def test_put_invalid_manager_extra(given: Given, when: When, then: Then):
    employee_type = given.an_employee_type()
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        'manager': {
            'name': 'A',
            'email': 'a@unit.test',
            'telephone': '07 999 000002',
            'employee_type_uid': employee_type['uid']
        }
    })
    then.bad_request_400()
    then.validation_messages({
        'manager': 'Unknown field.'
    })

def test_put_invalid_uid_extra(given: Given, when: When, then: Then):
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
        'uid': 42,
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001'
    })
    then.bad_request_400()
    then.validation_messages({
        'uid': 'Unknown field.'
    })

def test_put(given: Given, when: When, then: Then):
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001'
    })
    then.ok_200()
    then.json({
        'uid': practice['uid'],
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001'
    })

def test_put_get_multiple(given: Given, when: When, then: Then):
    manager_type = given.an_employee_type()

    first_manager = given.an_employee(of_type = manager_type['uid'])
    second_manager = given.an_employee(of_type = manager_type['uid'])

    first_practice = given.a_practice(with_manager = first_manager['uid'])
    second_practice = given.a_practice()

    when.put_practice(first_practice['uid'], {
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        'manager_uid': None
    })
    then.ok_200()

    when.put_practice(second_practice['uid'], {
        'name': 'Q',
        'address': '2 Unit Square, Exeter',
        'telephone': '07 999 000002',
        'manager_uid': second_manager['uid']
    })
    then.ok_200()

    when.get_all_practices()
    then.ok_200()
    then.json([
        {
            'uid': first_practice['uid'],
            'name': 'P',
            'address': '1 Unit Square, Exeter',
            'telephone': '07 999 000001'
        },
        {
            'uid': second_practice['uid'],
            'name': 'Q',
            'address': '2 Unit Square, Exeter',
            'telephone': '07 999 000002',
            'manager': second_manager
        }
    ])

    when.get_practice(first_practice['uid'])
    then.ok_200()
    then.json({
        'uid': first_practice['uid'],
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001'
    })

    when.get_practice(second_practice['uid'])
    then.ok_200()
    then.json({
        'uid': second_practice['uid'],
        'name': 'Q',
        'address': '2 Unit Square, Exeter',
        'telephone': '07 999 000002',
        'manager': second_manager
    })

# DELETE /practices/<int:id>
# -----------------------------------------------------------------------------

def test_delete_id_nonint(given: Given, when: When, then: Then):
    when.delete_practice('frog')
    then.not_found_404()

def test_delete_id_404(given: Given, when: When, then: Then):
    when.delete_practice('404')
    then.no_content_204() # Idempotent!

def test_delete_without_manager(given: Given, when: When, then: Then):
    first_practice = given.a_practice()
    second_practice = given.a_practice()

    when.get_all_practices()
    then.ok_200()
    then.json([
        first_practice,
        second_practice
    ])

    when.delete_practice(first_practice['uid'])
    then.no_content_204()

    when.get_all_practices()
    then.ok_200()
    then.json([
        second_practice
    ])

    when.get_practice(first_practice['uid'])
    then.not_found_404()

def test_delete_with_manager(given: Given, when: When, then: Then):
    manager_type = given.an_employee_type()
    manager = given.an_employee(of_type = manager_type['uid'])
    practice = given.a_practice(with_manager = manager['uid'])

    when.get_practice(practice['uid'])
    then.ok_200()

    when.get_employee(manager['uid'])
    then.ok_200()

    when.delete_practice(practice['uid'])
    then.no_content_204()

    when.get_practice(practice['uid'])
    then.not_found_404()

    when.get_employee(manager['uid'])
    then.ok_200()
