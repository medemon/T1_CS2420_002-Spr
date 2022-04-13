Employee Management System 1.0 - EMS has reached 1.0! Nearly feature complete and relatively stable!

	-To run this program you will need a working python interpreter with the pillow and tkcalender modules installed. 
	-Running the main program will attempt to install these modules if you do not have them.
	-Be sure to keep the folder structure for the EMS_1.0 folder intact, it is important!
	
	Simply run the Emp_Mgmt_System.py file through your python interpreter to start the program
	Ex: 'Python your/path/to/EMS_1.0/Emp_Mgmt_System.py' (replace your/path/to with actual path)

	Test login with admin privilages is ID: 377013 Password: Password123 (changed from default to avoid warning)
	Test login with an unprivilaged user ID: 165966 Password: AlvaradoRooney4659 (Password remained default to demonstrate the warning and password change feature)

Database:
	-The database runs off two files, the employee.csv file and passwords.csv (employees_base.csv is for dev purposes)
	-There are examples of both files in the system folder.
	-To generate a new examples, simply run the System_Control.py standalone then run Database_Manager.py to populate passwords.
	 (Warning! This will overwrite your employee.csv and passwords.csv files! back up and use wisely!)

1.0.1 Changes

	-Revamped the Payroll screen with the option to save reports to csv.
	-Added features to view and edit receipts and hours for commissioned and hourly employees. The hours screen is read only to non-admin users.
	-Search screen now excludes archived employees, now has the option to toggle archived if wanted.