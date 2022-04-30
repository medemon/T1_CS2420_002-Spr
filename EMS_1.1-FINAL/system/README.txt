Restart_system takes the original employees_base.csv file and adds all of the correct fields.
It generates all of the necessary fields, and can serve as a way to reset the system
if needed. All one would have to do is import restart_system.py from the Restart_system
folder and the entire database will be cleared.

It also manages the password file, and can clear it. Useful for development...
Loads the employee list and updates the file --> so things can be saved :)
Passwords are saved from the payroll.py file, but should probably be moved to the
system management file, so it is more loosely coupled
