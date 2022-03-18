Employee Management System 0.2.0

2/16/22

  Added full functionality for password database. Made user settings save on in file.

  Verification and validation
  Added class attributes for more information, 
  made a system file to help with development 
  (reset employee database, password database).
  
  Ready for GUI implementation

2/24/22

    Working on GUI Screens

    **Need to install pillow 'python3 -m pip install pillow' used for PNG Images**

2/27/22 -Don

	Replace the files in the main program with these three (I recommend making a copy) to test.

	I did not merge these with the main program because I did not want to risk overwriting anything Wyatt did.


	-Profile and Payroll screens are mostly functional. Needs some trash entry avoidance work and possibly cleanup on repetitive code.
	-Privileges are fixed and working in profile and payroll screens, change_frame does an admin check every screen change.
	-Use controller.admin boolean to check in the logged user is privileged.
	-Tweaked login to work with privileges. Needs fleshing out and a rework to match the UI design of the rest of the program
	-Slight edit to Search Screen to work with privileges and interface with profile screen, including adding employee
	-Fixed bugs and added missing components to the payroll.py and system_control.py files

3/17/22 - Don
	
	Program overhaul! Merged my and Wyatt's code, did much quality of life organizing to make the program neater as I will list:

	-The entire program now launches from the main program's main() like it should (meaning other modules act like proper modules now.)
	-Restructured the file layout. All reports are in the HourlyReports folder, all UI elements in UI and all system components are in the system folder. Only the main program in root file.
	-Renamed the main program to reflect what it is as Emp_Mgmt_System.py
	-Renamed payroll to Database_Manager.py to better reflect the roll as the database for our new program
	-Capitalized System_Control.py to match coding standards for modules/class files.
	-Found a Pathing solution that allows the program to run flawlessly with Unix based systems now. It appears to be bug free but to be sure, Windows users should hammer it to be sure.

	TODO:
	-Login still needs love. Looks basic.
	-Login assertion tests.
	-Search screen assertion tests
	-Report screen to match UI theme
	-Report screen assertion tests
	-Don is starting on 'trash-proofing' the entries for the profile screens
	-Don is starting on assertion tests for the profile screens