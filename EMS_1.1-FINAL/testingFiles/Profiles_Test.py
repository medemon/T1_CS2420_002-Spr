def test_all_profile_entries(ls, ps):
    '''Tests that all fields are what is in the emp object'''
    ls.id.set('688997')
    ls.pw.set('GayKarina9228')
    ls.submit_button.invoke()
    emp = ps.employee
    assert emp.first_name == ps.first_name.get()
    assert emp.last_name == ps.last_name.get()
    assert emp.address == ps.address.get()
    assert emp.city == ps.city.get()
    assert emp.state == ps.state.get()
    assert emp.zipcode == ps.zip.get()
    assert emp.phone == ps.phone.get()
    assert emp.DOB == ps.dob.get()
    assert emp.dept == ps.dept.get()
    assert emp.title == ps.title.get()
    assert emp.start_date == ps.start_date.get()
    assert emp.end_date == ps.end_date.get()
    assert emp.emp_id == ps.emp_id.get()
    assert int(emp.archived) == int(ps.archived.get())
    assert int(emp.admin) == int(ps.is_admin.get())

def test_user_permissions(ls, ps):
    '''Tests what fields users have and do not have access too in their own profile'''
    ls.id.set('522759')
    ls.pw.set('SnowTaShya5474')
    ls.submit_button.invoke()
    assert ps.first_name_entry.cget('state') == 'disabled'
    assert ps.last_name_entry.cget('state') == 'disabled'
    assert ps.address_entry.cget('state') == 'normal'
    assert ps.city_entry.cget('state') == 'normal'
    assert ps.state_drop.cget('state') == 'normal'
    assert ps.zip_entry.cget('state') == 'normal'
    assert ps.phone_entry.cget('state') == 'normal'
    assert str(ps.dob_entry.cget('state')) == 'disabled'
    assert ps.dept_entry.cget('state') == 'disabled'
    assert ps.title_entry.cget('state') == 'disabled'
    assert str(ps.start_date_entry.cget('state')) == 'disabled'
    assert str(ps.end_date_entry.cget('state')) == 'disabled'
    assert ps.archived_checkbox.cget('state') == 'disabled'
    assert ps.admin_checkbox.cget('state') == 'disabled'
    assert ps.payroll_button.cget('state') == 'normal'
    assert ps.save_button.cget('state') == 'normal'
    assert ps.password_button.cget('state') == 'normal'

def test_unprivilaged_permissions(ls, ps, app):
    '''Tests that users do not not have access too entires in other profiles'''
    ls.id.set('522759')
    ls.pw.set('SnowTaShya5474')
    ls.submit_button.invoke()
    app.select_employee('165966')
    assert ps.first_name_entry.cget('state') == 'disabled'
    assert ps.last_name_entry.cget('state') == 'disabled'
    assert ps.address_entry.cget('state') == 'disabled'
    assert ps.city_entry.cget('state') == 'disabled'
    assert ps.state_drop.cget('state') == 'disabled'
    assert ps.zip_entry.cget('state') == 'disabled'
    assert ps.phone_entry.cget('state') == 'disabled'
    assert str(ps.dob_entry.cget('state')) == 'disabled'
    assert ps.dept_entry.cget('state') == 'disabled'
    assert ps.title_entry.cget('state') == 'disabled'
    assert str(ps.start_date_entry.cget('state')) == 'disabled'
    assert str(ps.end_date_entry.cget('state')) == 'disabled'
    assert ps.archived_checkbox.cget('state') == 'disabled'
    assert ps.admin_checkbox.cget('state') == 'disabled'
    assert ps.payroll_button.cget('state') == 'disabled'
    assert ps.save_button.cget('state') == 'disabled'
    assert ps.password_button.cget('state') == 'disabled'

def test_admin_permissions(ls, ps, app):
    '''Tests that admin has access to all fields in another profile'''
    ls.id.set('688997')
    ls.pw.set('GayKarina9228')
    ls.submit_button.invoke()
    app.select_employee('165966')
    assert ps.first_name_entry.cget('state') == 'normal'
    assert ps.last_name_entry.cget('state') == 'normal'
    assert ps.address_entry.cget('state') == 'normal'
    assert ps.city_entry.cget('state') == 'normal'
    assert ps.state_drop.cget('state') == 'normal'
    assert ps.zip_entry.cget('state') == 'normal'
    assert ps.phone_entry.cget('state') == 'normal'
    assert str(ps.dob_entry.cget('state')) == 'normal'
    assert ps.dept_entry.cget('state') == 'normal'
    assert ps.title_entry.cget('state') == 'normal'
    assert str(ps.start_date_entry.cget('state')) == 'normal'
    ## end date varies on access to archived, if they have to that then they do this.
    #assert str(ps.end_date_entry.cget('state')) == 'normal'
    assert ps.archived_checkbox.cget('state') == 'normal'
    assert ps.admin_checkbox.cget('state') == 'normal'
    assert ps.payroll_button.cget('state') == 'normal'
    assert ps.save_button.cget('state') == 'normal'
    assert ps.password_button.cget('state') == 'normal'

def test_save_function(ls, ps):
    '''Tests that the save fuction writes changes to the employee object'''
    ls.id.set('165966')
    ls.pw.set('AlvaradoRooney4659')
    ls.submit_button.invoke()
    ps.first_name.set('Testies')
    ps.last_name.set('Testerson')
    ps.address.set('123 Fake St')
    ps.city.set('nowhere')
    ps.state.set('AZ')
    ps.zip.set('12345')
    ps.phone.set('1234567890')
    ps.dob.set('1/2/2001')
    ps.dept.set('home')
    ps.title.set('unemployed')
    ps.start_date.set('1/2/2001')
    ps.end_date.set('1/2/2001')
    ps.archived.set(1)
    ps.is_admin.set(1)
    ps.save_button.invoke()
    emp = ps.employee
    assert emp.first_name == 'Testies'
    assert emp.last_name == 'Testerson'
    assert emp.address == '123 Fake St'
    assert emp.city == 'nowhere'
    assert emp.state == 'AZ'
    assert emp.zipcode == '12345'
    assert emp.phone == '1234567890'
    assert emp.DOB == '01/02/2001'
    assert emp.dept == 'home'
    assert emp.title == 'unemployed'
    assert emp.start_date == '01/02/2001'
    assert emp.end_date == '01/02/2001'
    assert int(emp.archived) == 1
    assert int(emp.admin) == 1

def profiles_series(ls, ps, app):
    '''Test driver'''
    test_all_profile_entries(ls, ps)
    test_user_permissions(ls, ps)
    test_unprivilaged_permissions(ls, ps, app)
    test_admin_permissions(ls, ps, app)
    test_save_function(ls, ps)
    print("Profile pass!")