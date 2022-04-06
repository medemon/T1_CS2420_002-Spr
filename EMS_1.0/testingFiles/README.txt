Test scripts:
    All these tests were run against the sample employee_updated and password csv files. Place them into the system folder before running tests. ( and back up the current files if important!)
    
	To run the tests on Database_Manager and System_Control, place the Database_Manager_Test and System_Control_Test script in the system folder and run.

 To run the UI tests, go to the Emp_Mgmt_System.py script and uncomment the test fuction at the bottom, change testing to 1 and swap the commenting on main() and test()

    Because the test for the UI is designed to go through the UI like a user, it easier to have the main program run a test function than try to manage through a seperate script. This is acceptable because users won't be running these scripts.

    -Database_Manager_Test tests the functions of the Database_Manager.py script
    -System_Control_Test tests the funtions of the System_Control script
    -Login_Test tests the login screen, checking that it properly errors, successfully logs in and sets permissions.
    -Profiles_Test tests the profile screen, it checks that entries are properly loaded, changes are saved and permissions are correct for user, non-owner user and admin
    -PayScreen_Test tests the payroll profile screen, it checks that enteries are properly loated, changes are saved and permissions are correct for user and admin
    -Search_Test tests the search screen, it tests that search works by id, last name and first letter of last name, and tests that new employee initiates a new employee template in the profile screen
    -Report screen test was performed manually it displays the reports generated from the Database_Manager.