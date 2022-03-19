My old CS1410 program which we are turning into a fully executable GUI employee payroll software

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

    2/27/22

	Replace the files in the main program with these three (I recommend making a copy) to test.

	I did not merge these with the main program because I did not want to risk overwriting anything Wyatt did.


	-Profile and Payroll screens are mostly functional. Needs some trash entry avoidance work and possibly cleanup on repetitive code.
	-Privileges are fixed and working in profile and payroll screens, change_frame does an admin check every screen change.
	-Use controller.admin boolean to check in the logged user is privileged.
	-Tweaked login to work with privileges. Needs fleshing out and a rework to match the UI design of the rest of the program
	-Slight edit to Search Screen to work with privileges and interface with profile screen, including adding employee
	-Fixed bugs and added missing components to the payroll.py and system_controll.py files