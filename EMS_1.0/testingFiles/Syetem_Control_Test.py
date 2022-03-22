from pathlib import Path
import System_Control as s
from types import NoneType
"""Test file for the syetem control - which formats our database"""

def testFourRandom():
    """Testing our four_random function to make sure it returns no errors, and an int type"""
    dummyFour = s.four_random()
    assert isinstance(dummyFour, int)

    #Making sure it is 4 in length
    assert len(str(dummyFour)) == 4

def testThreeRandom():
    """Testing our three_random function to make sure it returns no errors and an int type"""
    dummyThree = s.three_random()
    assert isinstance(dummyThree, int)

    #Making sure it is 3 in length
    assert len(str(dummyThree)) == 3

def testTwoRandom():
    """Testing our two_random function to make sure it returns no errors and an int type"""
    dummyTwo = s.two_random()
    assert isinstance(dummyTwo, int)

    #Making sure it is 2 in length
    assert len(str(dummyTwo)) == 2

def testGeneratePhoneNumber():
    """Testing our generate_phone_number function to make sure it returns a string and no errors"""
    dummyNum = s.generate_phone_number()
    assert isinstance(dummyNum, str)

    #Checking the format of the number to make sure it is the correct format
    assert dummyNum[3] == '-' and dummyNum[7] == '-'

    #Making sure out phone number is the appropriate length
    assert len(dummyNum) == 12

def testGenerateSSN():
    """Testing our generate_SSN function to make sure it returns a string and no errors"""
    dummySSN = s.generate_SSN()
    assert isinstance(dummySSN, str)

    #Making sure that the SSN is the appropriate format
    assert dummySSN[3] == '-' and dummySSN[6] == '-'

    #Making sure that the SSN generated is the appropriate length
    assert len(dummySSN) == 11

def testGenerateDOB():
    """Testing our generate_DOB function to make sure it returns a string and no errors"""
    dummyDOB = s.generate_DOB()
    assert isinstance(dummyDOB, str)

    #Making sure our DOB has the items necessary
    assert '/' in dummyDOB


def testGenerateDate():
    """Testing our generate_date function to make sure it returns a string and no errors"""
    dummyDate = s.generate_date()
    assert isinstance(dummyDate, str)

    #Making sure our generated date matches the appropriate format
    assert (len(dummyDate) == 8)

    #Making sure that the date if formatted with dashes correctly
    assert dummyDate[2] == '/' and dummyDate[5] == '/'


def testGenerateTitle():
    """Testing our generate_title function to make sure it returns a string and no errors"""
    dummyTitle = s.generate_title()
    assert isinstance(dummyTitle, str)

    #Making sure our title is in the list of titles
    titles = ["Supervisor", "Employee"]
    assert dummyTitle in titles

def testGenerateDepartment():
    """Testing our generate_department function to make sure it returns a string with no errors"""
    dummyDept = s.generate_department()
    assert isinstance(dummyDept, str)

    #Making sure returned data is correct and in the list of departments
    assert dummyDept in ["Low Level Design Department", "Digital design Department", "Statistics Department"]

def testRestartSystem():
    """Testing our restart_system function to make sure it returns void, and does what is asked"""
    dummyReset = s.restart_system() #Restarting the system - employees file, passwords, etc.
    assert isinstance(dummyReset, NoneType)

    #Making sure that our resetted passwords file is correctly formatted
    password_file = Path(__file__).resolve().parent / 'passwords.csv'
    lines_list =[]
    with open(password_file, 'r') as f:
        for i in f:
            lines_list.append(i.split(','))
        #Making sure the column titles are appropriate
        assert lines_list[0][0] == "Username" 
        assert lines_list[0][1] == " Password\n"

        #Making sure that the column values are correct for no passwords being set
        assert "None" in lines_list[1][1]


    #Making sure that our new employees file is correctly formatted in its column
    employees_file = Path(__file__).resolve().parent / 'employees_updated.csv'
    with open(employees_file, 'r') as f:
        assert "ID,first,last,Address,City,State,Zip,Classification,PayMethod,Salary,Hourly,Commission,Route,Account,Phone,SSN,DOB,Start_Date,End_Date,Title,Department,Archived,Admin\n" in f.read()



if __name__ == "__main__":
    testFourRandom()
    testThreeRandom()
    testTwoRandom()
    testGeneratePhoneNumber()
    testGenerateSSN()
    testGenerateDOB()
    testGenerateDate()
    testGenerateTitle()
    testGenerateDepartment()
    testRestartSystem()
    print("System Control Pass!")

