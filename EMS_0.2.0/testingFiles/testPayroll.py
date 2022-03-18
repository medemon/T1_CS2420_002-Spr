from types import NoneType
import payroll as p
""" -PUT IN THE SAME DIRECTORY AS PAYROLL.PY
    -Testing for different errors, if the assertion fails it will raise an error and not return None type"""

# Test profile is Karina Gay w/ employee ID: 688997


def testSetPassword():
    """Testing the set_password function in payroll.py"""
    #Testing that the set_password function will accept all data types as password
    assert isinstance(p.set_password(688997, 'Bananas1234'), NoneType)
    assert isinstance(p.set_password(688997, 59834759), NoneType)
    #Testing that the set_password function will accept all data types as user ID
    assert isinstance(p.set_password(688997, 'Test'), NoneType)
    assert isinstance(p.set_password('688997', 'Test'), NoneType)

def testGetPassword():
    """Testing the get_password in payroll.py"""
    #Checking to see that different types for employee ID does not throw an error
    assert isinstance(p.get_password(688997), str)
    assert isinstance(p.get_password('688997'), str)

def testEmployeeObject():
    """Testing the employee object and its new methods"""
    #loading employee via load_employees function
    p.load_employees()
    dummyEmp = p.total_employees[0]

    #Testing that get password method returns a string
    assert isinstance(dummyEmp.get_password(), str)

    #Testing that archive employee throws no errors and returns None
    assert isinstance(dummyEmp.archive_employee(False), NoneType)

    #Testing that set default password method returns no errors and returns None
    assert isinstance(dummyEmp.set_default_password(), NoneType)

    #Testing that set password method throws no errors and returns None
    assert isinstance(dummyEmp.set_password('Bananas'), NoneType)


def testFindEmployeeByPartialId():
    """Testing the find_employee_by_partial_id for search query function"""
    #Testing that the query function does not throw any errors
    assert isinstance(p.find_employee_by_partial_id('6'), list)

def testFindEmployeeByLastNameFiltered():
    """Testing the filtered get employee by last name function"""
    #creating a dummy employee to test the function
    p.load_employees()
    dummyEmp = p.total_employees[0]
    #making sure function throws no errors and returns expected type
    assert isinstance(p.find_employee_by_last_name_filtered('Gay', [dummyEmp]), list)

def testFindEmployeeByLastNameTotal():
    """Testing the find employee by last name total function"""
    p.load_employees()
    assert isinstance(p.find_employee_by_last_name_total('G'), list)



def globalVariables():
    """Tests the global variables to make sure they are correct"""
    #Testing paylog file name
    assert (p.PAY_LOGFILE == 'paylog.txt')
    #Testing that total_employees is an empty list
    assert (isinstance(p.total_employees, list))

def testFindEmployeeByLastNameTotal():
    #p.find_employee_by_last_name_total making sure the function throws no errors
    assert isinstance(p.find_employee_by_last_name_total('Gay'), list)

    





if __name__ == "__main__":
    """If NO error raises, program is good to be run"""
    testSetPassword() #Testing the set_password function
    testGetPassword()  #Testing the get_password function
    testEmployeeObject() #Testing the new Employee methods
    testFindEmployeeByPartialId() #Testing the query search function
    testFindEmployeeByLastNameFiltered() #Test the last name filter function
    testFindEmployeeByLastNameTotal() #Test the total last name unfiltered function
    globalVariables() #Testing the global variables 
    testFindEmployeeByLastNameTotal() 


