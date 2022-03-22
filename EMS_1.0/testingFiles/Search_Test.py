def test_search_results(ls, ps, ss):
    '''Tests search by ID, by lastname and by first letter of last name'''
    ls.id.set('688997')
    ls.pw.set('GayKarina9228')
    ls.submit_button.invoke()
    ps.search_button.invoke()
    ss.emp_ID.set('522759')
    ss.search_button.invoke()
    result = ss.retrieved_employees[0]
    assert result.emp_id == '522759'
    ss.emp_ID.set('')
    ss.last_name.set('Pitts')
    ss.search_button.invoke()
    result = ss.retrieved_employees[0]
    assert result.emp_id == '939825'
    ss.last_name.set('W')
    ss.search_button.invoke()
    results = []
    for i in ss.retrieved_employees:
        results.append(i.emp_id)
    key = ['163695','285767','426824']
    assert all(elem in results for elem in key)

def add_employee_test(ls, ps, ss):
    '''Tests that the add employee button opens a new employee templet'''
    ls.id.set('688997')
    ls.pw.set('GayKarina9228')
    ls.submit_button.invoke()
    ps.search_button.invoke()
    ss.new_employee_button.invoke()
    assert ps.first_name.get() == ''
    assert ps.last_name.get() == ''
    assert ps.address.get() == ''
    assert ps.city.get() == ''
    assert ps.state.get() == ''
    assert ps.zip.get() == ''
    assert ps.phone.get() == ''
    assert ps.dob.get() == ''
    assert ps.dept.get() == ''
    assert ps.title.get() == ''
    assert ps.start_date.get() == ''
    assert ps.end_date.get() == ''
    assert int(ps.archived.get()) == 0
    assert int(ps.is_admin.get()) == 0

def search_series(ls, ps, ss):
    '''Test driver'''
    test_search_results(ls, ps, ss)
    add_employee_test(ls, ps, ss)
    print('Search Pass!')