from tests.utils import Given, Then, When

# PUT /practices/<int:id>/manager/<int:id>
# -----------------------------------------------------------------------------

def test_put_invalid_id_non_int(given: Given, when: When, then: Then):
    practice = given.a_practice()
    manager = given.an_employee(in_practice = practice['uid'])

    when.put_practice_manager('frog', 'frog')
    then.not_found_404()

    when.put_practice_manager('frog', manager['uid'])
    then.not_found_404()

    when.put_practice_manager(practice['uid'], 'frog')
    then.not_found_404()

def test_put_invalid_id_404(given: Given, when: When, then: Then):
    practice = given.a_practice()
    manager = given.an_employee(in_practice = practice['uid'])

    when.put_practice_manager('404', '404')
    then.not_found_404()

    when.put_practice_manager('404', manager['uid'])
    then.not_found_404()

    when.put_practice_manager(practice['uid'], '404')
    then.not_found_404()

def test_put_invalid_manager_from_another_practice(given: Given, when: When, then: Then):
    first_practice = given.a_practice()
    second_practice = given.a_practice()

    manager = given.an_employee(in_practice = first_practice['uid'])

    when.put_practice_manager(second_practice['uid'], manager['uid'])
    then.conflict_409()
    then.error_message('Manager works in another practice.')

def test_put(given: Given, when: When, then: Then):
    practice = given.a_practice()
    manager = given.an_employee(in_practice = practice['uid'])

    when.put_practice_manager(practice['uid'], manager['uid'])
    then.no_content_204()

    manager['practice']['manager'] = manager.copy()
    del manager['practice']['manager']['practice']

    when.get_employee(manager['uid'])
    then.ok_200()
    then.json(manager)

    practice['manager'] = manager
    del practice['manager']['practice']

    when.get_practice(practice['uid'])
    then.ok_200()
    then.json(practice)

def test_put_idempotent(given: Given, when: When, then: Then):
    practice = given.a_practice()
    manager = given.an_employee(in_practice = practice['uid'])

    when.put_practice_manager(practice['uid'], manager['uid'])
    then.no_content_204()

    when.put_practice_manager(practice['uid'], manager['uid']) # Idempotent!
    then.no_content_204()

    manager['practice']['manager'] = manager.copy()
    del manager['practice']['manager']['practice']

    when.get_employee(manager['uid'])
    then.ok_200()
    then.json(manager)

    practice['manager'] = manager
    del practice['manager']['practice']

    when.get_practice(practice['uid'])
    then.ok_200()
    then.json(practice)

# DELETE /practices/<int:id>/manager/
# -----------------------------------------------------------------------------

def test_delete_invalid_id_non_int(given: Given, when: When, then: Then):
    when.delete_practice_manager('frog')
    then.not_found_404()

def test_delete_invalid_id_404(given: Given, when: When, then: Then):
    when.delete_practice_manager('404')
    then.not_found_404()

def test_delete(given: Given, when: When, then: Then):
    practice, manager = given.a_practice_with_a_manager()

    when.delete_practice_manager(practice['uid'])
    then.no_content_204()

    when.get_practice(practice['uid'])
    then.ok_200()
    practice = then().json

    when.get_employee(manager['uid'])
    then.ok_200()
    manager = then().json

    assert practice.get('manager') is None # The practice looses its manager...
    assert manager['practice']['uid'] == practice['uid'] # ... but the manager still works at the practice!

def test_delete_idempotent(given: Given, when: When, then: Then):
    practice, manager = given.a_practice_with_a_manager()

    when.delete_practice_manager(practice['uid'])
    then.no_content_204()

    when.delete_practice_manager(practice['uid']) # Idempotent!
    then.no_content_204()

    when.get_practice(practice['uid'])
    then.ok_200()
    practice = then().json

    when.get_employee(manager['uid'])
    then.ok_200()
    manager = then().json

    assert practice.get('manager') is None # The practice looses its manager...
    assert manager['practice']['uid'] == practice['uid'] # ... but the manager still works at the practice!
