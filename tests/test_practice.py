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
        # 'employee_type_uid': 'frog'
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Not a valid string.',
        'address': 'Not a valid string.',
        'telephone': 'Not a valid string.',
        # 'employee_type_uid': 'Not a valid integer.'
    })

def test_post_invalid_2(given: Given, when: When, then: Then):
    when.post_practice({
        'name': '',
        'address': '',
        'telephone': '',
        # 'employee_type_uid': 404
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Length must be between 1 and 70.',
        'address': 'Length must be between 1 and 255.',
        'telephone': 'Length must be between 1 and 32.',
        # 'employee_type_uid': 'Not referencing an existing resource.'
    })

def test_post_invalid_3(given: Given, when: When, then: Then):
    when.post_practice({
        'name': None,
        'address': None,
        'telephone': None,
        # 'employee_type_uid': None
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Field may not be null.',
        'address': 'Field may not be null.',
        'telephone': 'Field may not be null.',
        # 'employee_type_uid': 'Field may not be null.'
    })

def test_post_invalid_4(given: Given, when: When, then: Then):
    when.post_practice({
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Missing data for required field.',
        'address': 'Missing data for required field.',
        'telephone': 'Missing data for required field.',
        # 'employee_type_uid': 'Missing data for required field.'
    })

def test_post_invalid_5(given: Given, when: When, then: Then):
    when.post_practice({
        'name': 'X' * 71,
        'address': 'X' * 256,
        'telephone': 'X' * 33,
        # 'employee_type_uid': 404
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Length must be between 1 and 70.',
        'address': 'Length must be between 1 and 255.',
        'telephone': 'Length must be between 1 and 32.',
        # 'employee_type_uid': 'Not referencing an existing resource.'
    })

def test_post_invalid_uid_extra(given: Given, when: When, then: Then):
    when.post_practice({
        'uid': 42,
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        # 'employee_type_uid': 404
    })
    then.bad_request_400()
    then.validation_messages({
        'uid': 'Unknown field.',
        # 'employee_type_uid': 'Not referencing an existing resource.'
    })

# def test_post_invalid_employee_type_extra(given: Given, when: When, then: Then):
#     when.post_practice({
#         'name': 'P',
#         'address': '1 Unit Square, Exeter',
#         'telephone': '07 999 000001',
#         'employee_type': {
#             'type': 'T'
#         }
#     })
#     then.bad_request_400()
#     then.validation_messages({
#         'employee_type': 'Unknown field.'
#     })

def test_post(given: Given, when: When, then: Then):
    # employee_type = given.an_employee_type()

    when.post_practice({
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        # 'employee_type_uid': employee_type['uid']
    })
    then.created_201()
    then.json({
        'uid': 1,
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        # 'employee_type': employee_type
    })

def test_post_get_multiple(given: Given, when: When, then: Then):
    # first_type = given.an_employee_type()
    # second_type = given.an_employee_type()

    first = given.a_practice()
    second = given.a_practice()

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
    # employee_type = given.an_employee_type()

    when.put_practice('frog', {
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        # 'employee_type_uid': employee_type['uid']
    })
    then.not_found_404()

def test_put_id_404(given: Given, when: When, then: Then):
    # employee_type = given.an_employee_type()

    when.put_practice('404', {
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        # 'employee_type_uid': employee_type['uid']
    })
    then.not_found_404()

def test_put_invalid_1(given: Given, when: When, then: Then):
    # employee_type = given.an_employee_type()
    # employee = given.an_employee(of_type = employee_type['uid'])
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
        'name': 42,
        'address': 42,
        'telephone': 42,
        # 'employee_type_uid': 'frog'
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Not a valid string.',
        'address': 'Not a valid string.',
        'telephone': 'Not a valid string.',
        # 'employee_type_uid': 'Not a valid integer.'
    })

def test_put_invalid_2(given: Given, when: When, then: Then):
    # employee_type = given.an_employee_type()
    # employee = given.an_employee(of_type = employee_type['uid'])
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
        'name': '',
        'address': '',
        'telephone': '',
        # 'employee_type_uid': 404
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Length must be between 1 and 70.',
        'address': 'Length must be between 1 and 255.',
        'telephone': 'Length must be between 1 and 32.',
        # 'employee_type_uid': 'Not referencing an existing resource.'
    })

def test_put_invalid_3(given: Given, when: When, then: Then):
    # employee_type = given.an_employee_type()
    # employee = given.an_employee(of_type = employee_type['uid'])
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
        'name': None,
        'address': None,
        'telephone': None,
        # 'employee_type_uid': None
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Field may not be null.',
        'address': 'Field may not be null.',
        'telephone': 'Field may not be null.',
        # 'employee_type_uid': 'Field may not be null.'
    })

def test_put_invalid_4(given: Given, when: When, then: Then):
    # employee_type = given.an_employee_type()
    # employee = given.an_employee(of_type = employee_type['uid'])
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Missing data for required field.',
        'address': 'Missing data for required field.',
        'telephone': 'Missing data for required field.',
        # 'employee_type_uid': 'Missing data for required field.'
    })

def test_put_invalid_5(given: Given, when: When, then: Then):
    # employee_type = given.an_employee_type()
    # employee = given.an_employee(of_type = employee_type['uid'])
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
        'name': 'X' * 71,
        'address': 'X' * 256,
        'telephone': 'X' * 33,
        # 'employee_type_uid': 404
    })
    then.bad_request_400()
    then.validation_messages({
        'name': 'Length must be between 1 and 70.',
        'address': 'Length must be between 1 and 255.',
        'telephone': 'Length must be between 1 and 32.',
        # 'employee_type_uid': 'Not referencing an existing resource.'
    })

# def test_put_invalid_employee_type_extra(given: Given, when: When, then: Then):
#     employee_type = given.an_employee_type()
#     employee = given.an_employee(of_type = employee_type['uid'])
#     practice = given.a_practice()
#
#     when.put_practice(practice['uid'], {
#         'name': 'P',
#         'address': '1 Unit Square, Exeter',
#         'telephone': '07 999 000001',
#         'employee_type': {
#             'type': 'T'
#         }
#     })
#     then.bad_request_400()
#     then.validation_messages({
#         'employee_type': 'Unknown field.'
#     })

def test_put_invalid_uid_extra(given: Given, when: When, then: Then):
    # employee_type = given.an_employee_type()
    # employee = given.an_employee(of_type = employee_type['uid'])
    practice = given.a_practice()

    when.put_practice(practice['uid'], {
        'uid': 42,
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        # 'employee_type_uid': employee_type['uid']
    })
    then.bad_request_400()
    then.validation_messages({
        'uid': 'Unknown field.'
    })

def test_put(given: Given, when: When, then: Then):
#     first_type = given.an_employee_type()
#     second_type = given.an_employee_type()
#
#     employee = given.an_employee(of_type = first_type['uid'])

    practice = given.a_practice()

    when.put_practice(practice['uid'], {
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        # 'employee_type_uid': second_type['uid']
    })
    then.ok_200()
    then.json({
        'uid': practice['uid'],
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        # 'employee_type': second_type
    })

def test_put_get_multiple(given: Given, when: When, then: Then):
#     first_type = given.an_employee_type()
#     second_type = given.an_employee_type()
#
#     first_employee = given.an_employee(of_type = first_type['uid'])
#     second_employee = given.an_employee(of_type = second_type['uid'])

    first_practice = given.a_practice()
    second_practice = given.a_practice()

    when.put_practice(second_practice['uid'], {
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        # 'employee_type_uid': first_type['uid']
    })

    when.get_practice(second_practice['uid'])
    then.ok_200()
    then.json({
        'uid': second_practice['uid'],
        'name': 'P',
        'address': '1 Unit Square, Exeter',
        'telephone': '07 999 000001',
        # 'employee_type': first_type
    })

    when.get_all_practices()
    then.ok_200()
    then.json([
        first_practice,
        {
            'uid': second_practice['uid'],
            'name': 'P',
            'address': '1 Unit Square, Exeter',
            'telephone': '07 999 000001',
            # 'employee_type': first_type
        }
    ])

# DELETE /practices/<int:id>
# -----------------------------------------------------------------------------

def test_delete_id_nonint(given: Given, when: When, then: Then):
    when.delete_practice('frog')
    then.not_found_404()

def test_delete_id_404(given: Given, when: When, then: Then):
    when.delete_practice('404')
    then.no_content_204() # Idempotent!

def test_delete(given: Given, when: When, then: Then):
    # employee_type = given.an_employee_type()

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
