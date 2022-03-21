
def login_errors_test(ls):
    '''tests the user ID input and lookup as well password input and sees if the login screen is properly catching invalid entries'''
    ls.submit_button.invoke()
    assert ls.msg.get() == "Invalid Employee ID!"
    ls.id.set('Derp')
    ls.submit_button.invoke()
    assert ls.msg.get() == "Invalid Employee ID!"
    ls.id.set('688997')
    ls.submit_button.invoke()
    assert ls.msg.get() == "Invalid password!"
    ls.pw.set('ABC123')  
    ls.submit_button.invoke()
    assert ls.msg.get() == "Invalid password!"

def user_login_success(ls):
    '''Tests if the login is successful with correct credentials'''
    ls.id.set('688997')
    ls.pw.set('GayKarina9228')
    ls.submit_button.invoke()
    assert ls.msg.get() == "Success!"

def test_admin(ls,app):
    '''Tests if admin rights are properly flagged upon login'''
    ls.id.set('688997')
    ls.pw.set('GayKarina9228')
    ls.submit_button.invoke()
    assert app.admin.get() == True
    ls.id.set('522759')
    ls.pw.set('SnowTaShya5474')
    ls.submit_button.invoke()
    assert app.admin.get() == False

def login_series(ls, app):
    '''Test runner'''
    login_errors_test(ls)
    user_login_success(ls)
    test_admin(ls, app)
    print("All pass!")