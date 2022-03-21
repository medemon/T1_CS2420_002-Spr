def test_all_profile_entries(ls, ps, eps, app):
    '''Tests that all fields are what is in the emp object'''
    ls.id.set('688997')
    ls.pw.set('GayKarina9228')
    ls.submit_button.invoke()
    emp = ps.employee
    ps.payroll_button.invoke()
    assert emp.route == eps.routing.get()
    assert emp.accounting == eps.account.get()
    assert emp.SSN == eps.ssn.get()
    assert int(emp.payment_method) == 1
    assert int(emp.classification) == 1
    assert eps.salary.get() == emp.pay_rates[0]
    # for commission
    app.select_employee('522759')
    emp = ps.employee
    ps.payroll_button.invoke()
    assert int(emp.classification) == 2
    assert eps.salary.get() == emp.pay_rates[0]
    assert eps.rate.get() == emp.pay_rates[2]
    # for hourly
    app.select_employee('265154')
    emp = ps.employee
    ps.payroll_button.invoke()
    assert int(emp.classification) == 3
    assert eps.rate.get() == emp.pay_rates[1]

def test_user_permissions(ls, ps, eps):
    '''Tests what fields users have and do not have access too in their own profile'''
    ls.id.set('522759')
    ls.pw.set('SnowTaShya5474')
    ls.submit_button.invoke()
    ps.payroll_button.invoke()
    assert eps.ssn_entry.cget('state') == 'disabled'
    assert eps.classy_drop.cget('state') == 'disabled'
    assert eps.salary_entry.cget('state') == 'disabled'
    assert eps.rate_entry.cget('state') == 'disabled'
    assert eps.pay_method_drop.cget('state') == 'normal'
    assert eps.routing_entry.cget('state') == 'normal'
    assert eps.account_entry.cget('state') == 'normal'

def test_admin_permissions(ls, ps, eps, app):
    '''Tests that admin has access to all fields in another profile'''
    ls.id.set('688997')
    ls.pw.set('GayKarina9228')
    ls.submit_button.invoke()
    app.select_employee('165966')
    ps.payroll_button.invoke()
    assert eps.ssn_entry.cget('state') == 'normal'
    assert eps.classy_drop.cget('state') == 'normal'
    assert eps.rate_entry.cget('state') == 'normal'
    assert eps.pay_method_drop.cget('state') == 'normal'
    assert eps.routing_entry.cget('state') == 'normal'
    assert eps.account_entry.cget('state') == 'normal'


def test_save_function(ls, ps, eps):
    ls.id.set('165966')
    ls.pw.set('AlvaradoRooney4659')
    ls.submit_button.invoke()
    emp = ps.employee
    ps.payroll_button.invoke()
    eps.classy.set(3)
    eps.pay_method.set("Direct Deposit")
    eps.ssn.set('123456789')
    eps.rate.set('1.00')
    eps.routing.set('30417353-K')
    eps.account.set('465794-3611')
    eps.save_button.invoke()
    assert emp.route == '30417353-K'
    assert emp.accounting == '465794-3611'
    assert emp.SSN == '123456789'
    assert int(emp.payment_method) == 2
    assert int(emp.classification) == 3
    assert eps.rate.get() == '1.00'

def payscreen_series(ls, ps, eps, app):
    test_all_profile_entries(ls, ps, eps, app)
    test_user_permissions(ls, ps, eps)
    test_admin_permissions(ls, ps,eps, app)
    test_save_function(ls, ps, eps)
    print("PayScreen pass!")