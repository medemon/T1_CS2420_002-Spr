'''Back end for main program which handles all of the databases and employees'''

# import modules
from abc import ABC, abstractmethod  # used to make abstract classes and methods
import os, os.path
# System control to reset employees.csv or password database
import system.system_control as system

# vars
PAY_LOGFILE = 'paylog.txt'  # saved file to write to

# list dictionaries
total_employees = []  # list for all employee objects or instances


# Password management functions
def set_password(user_ID, new_password):
    """This function will find the user in the password database and change the password associated with their ID"""

    # Can make it raise an exception for error analysis if the password is not a specific length and return a value which will tell wyatt's
    # Screen to show the user they can't change the password to that
    # That way it does not change anything and his window will know what to do

    # V&V for Wyatt so he can put ints or strings in through the functions :)
    if type(user_ID) != str:
        user_ID = str(user_ID)

    # V&V to make sure that Wyatt can pass whatever type through :)
    if type(new_password) != str:
        new_password = str(new_password)

    # OK now here is the tough part, we need to find the correlating user ID and rewrite the whole file as it was before..
    # So we will just replace the given username and password tuple, list whatever you want to call it with the corrected
    # one and then we can just write the file again the right way

    passwords_file = os.path.dirname(__file__) + '\\system\\passwords.csv'
    # Open the passwords file first, save the list of lists of user names and passwords
    # Change the corresponding list, save it, write the whole file again
    users_and_passwords = []
    with open(passwords_file, 'r') as f:
        temp = f.read().splitlines()
        for items in temp:
            users_and_passwords.append(items.split(','))

    # Ok now we have loaded the usernames and passwords, now it is time to change the appropriate password
    for items in users_and_passwords:
        if items[0] == user_ID:
            items[1] = new_password

    # Okay now write all that to replace the file sweetie <3
    with open(passwords_file, 'w') as f:
        for i in users_and_passwords:
            f.write(f"{i[0]},{i[1]}\n")


def get_password(user_ID):
    """Grabs the password from the database file by User ID. This will be so that we can load previously saved passwords for employees."""
    # V&V to make it so that function can have both int parameters and string parameters
    # Because when parsing the file, it will come out as a string by default
    # This is to ensure Wyatt does not run into any issues when coding the front end :)
    if type(user_ID) == int:
        user_ID = str(user_ID)

    # Password file is in the correct spot inside of system
    # The restart_system file will automatically create a file for password
    # When it is run! Be careful, it will reset the whole system if function is run.
    passwords_file = os.path.dirname(__file__) + '\\system\\passwords.csv'

    # Potential security threat is having this run in the main program because it will become avalible
    # In the RAM while the program is running

    # Users and passwords will be a list of lists which contain the ID on the first index, and password on the second
    # Formatted like so [[123123,bananas], [123123,password]] so yeah
    users_and_passwords = []
    with open(passwords_file, 'r') as f:
        temp = f.read().splitlines()
        for items in temp:
            users_and_passwords.append(items.split(','))

    # Now we need to scan through the lists and find which ID matches the given password
    # Just using a linear search but in a giant database this would not be optimal
    for auth in users_and_passwords:
        if auth[0] == user_ID:
            return auth[1]
    # Returns the given password


# Original classes
class Classification(ABC):
    # abstract class for Commissioned, Salaried, Hourly

    @abstractmethod
    def issue_payment(self):  # abstract method that is required to be over written
        pass


class Employee:
    '''Employee class takes several attributes when instantiating. Each employee
        has an id, first, last name, full address, and lastly what type of employee he or she is...
        this includes Salaried, Commissioned, or Hourly.'''

    def __init__(self, emp_id, first_name, last_name, address, city, state, \
                 zipcode, classification, payment_method, pay_rates, route, accounting, phone, SSN, \
                 DOB, start, end, title, dept, archived, admin):

        self.emp_id = emp_id  # employee id
        self.first_name = first_name  # first name
        self.last_name = last_name  # last name
        self.address = address  # address
        self.city = city  # city
        self.state = state  # state
        self.zipcode = zipcode  # zipcode
        self.classification = classification  # 1=Salaried, 2=Commissioned, 3=Hourly
        self.payment_method = payment_method  # 1=Mailed 2=Wired
        self.pay_rates = pay_rates # List of pay rates: [0]Salary, [1]Commission, [2]Hourly
        self.route = route  # This is the routing number if employee choses to have pay delivered electronically
        self.accounting = accounting  # This is the accounting number if employee choses pay electronically
        self.phone = phone  # This is the personal phone
        self.SSN = SSN  # This is the employee's social security number
        self.DOB = DOB  # This is the employee's birthday hooooray
        self.start_date = start  # Date employee started
        self.end_date = end  # Date employee ended (randomly generated w/ small odds)
        self.title = title  # Title of job desc
        self.dept = dept  # Dept where employee belongs
        self.password = ''  # Intentionally
        self.archived = archived # Archived boolean
        self.admin = admin  # Admin boolean

    def get_password(self):
        return get_password(self.emp_id)

    def archive_employee(self, bool_var):
        """"Method to toggle archive in employee"""
        self.archived = bool_var
    
    def set_admin(self, bool_var):
        """"Method to toggle archive in employee"""
        self.admin = bool_var

    def set_default_password(self):
        """"Method to set default password in employee file if employee has none"""
        self.password = set_password(self.emp_id, f"{self.last_name}{self.first_name}{self.SSN[-4:]}")

    def set_password(self, new_password):
        self.password = set_password(self.emp_id, new_password)

    def make_salaried(self, salary):  # 1: instantiates Salaried class in attribute
        self.classification = Salaried(salary)

    def make_commissioned(self, salary, comm_rate=0):  # 2: instantiates Commissioned class in attribute
        self.classification = Commissioned(salary, comm_rate)

    def make_hourly(self, hourly_rate):  # 3: instantiates Hourly class in attribute
        self.classification = Hourly(hourly_rate)

    def issue_pay(self, payroll):
        '''This method writes to the file of how much each employee will be paid. Goes through
        all employees and only writes to the file the employees that will be making money. This function
        takes the amount returned from the emp.classification.issue_payment() method.'''
        if float(payroll) == 0:  # if the employee did not make anything, no payment is written to file
            pass
        else:
            paylog_file = os.path.dirname(__file__) + '\\HoursReports\\paylog.txt'
            with open(paylog_file, 'a+') as f:  # a+ appends to the file
                if self.payment_method == str(1):
                    f.write(f"Mailing {payroll} to {self.first_name} {self.last_name}" \
                            f" at {self.address} {self.city} {self.state} {self.zipcode}\n")
                else:
                    f.write(f"Wiring {payroll} to {self.first_name} {self.last_name}" \
                            f" to a bank account routing: {self.route} accounting: {self.accounting}\n")


class Salaried(Classification):
    '''This class has one attribute which is the salary.'''

    def __init__(self, salary):
        self.salary = float(salary)

    def issue_payment(self):
        '''1/24 of the salary will be paid and the amount is returned.'''
        pay = self.salary / 24
        return format(round(pay, 2), '.2f')

    def __str__(self):
        return 'Salaried'

    def __int__(self):
        return 1

class Commissioned(Salaried):
    '''This class takes two attributes, salary since Commissioned is the child class to Salaried
and the rate of commission. The rate is by default set to zero.'''

    def __init__(self, salary, comm_rate=0):
        Salaried.__init__(self, salary)
        self.comm_rate = int(float(comm_rate))
        self.receipts = []  # member to store all receipts for the employee

    def __str__(self):
        return 'Commissioned'
    
    def __int__(self):
        return 2

    def issue_payment(self):
        '''Stores the 1/24 of the total of the salary then adds up any receipts and multiplies the
sum by the rate to add to the total. The total amount is returned. The receipts list is cleared
each call to avoid paying the employee multiple payments.'''
        total = self.salary / 24
        rate = self.comm_rate * 0.01
        add_on = sum(list(map(float, self.receipts))) * rate
        total += add_on
        self.receipts = []
        return format(round(total, 2), '.2f')

    def add_receipts(self, num):
        '''Adds a receipt to the receipt list.'''
        self.receipts.append(num)


class Hourly(Classification):
    '''This class takes one attribute which is the rate at which the employee is paid per hour.'''

    def __init__(self, hourly_rate):
        self.hourly_rate = int(float(hourly_rate))
        self.timecard = []  # list to keep track of hours worked

    def issue_payment(self):
        '''Multiplies and adds up all the hours from the timecard. Returns the total amount. The
timecard list is cleared.'''
        total = 0
        for num in self.timecard:
            money = float(num) * self.hourly_rate
            total += money
        self.timecard = []
        return format(round(total, 2), '.2f')

    def add_timecard(self, num):
        '''Adds hour amount to the timecard list.'''
        self.timecard.append(num)

    def __str__(self):
        return 'Hourly'

    def __int__(self):
        return 3


def load_employees():
    '''Reads the employee file and stores all employees with the correct information in a list of
objects.'''
    employees_file = os.path.dirname(__file__) + '\\system\\employees_updated.csv'
    with open(employees_file, 'r') as f:
        i = 0
        data = f.readlines()
        for line in data:
            if i == 0:
                i += 1
            else:
                info = line.split(',')
                id_num = info[0]
                first = info[1]
                last = info[2]
                addy = info[3]
                city = info[4]
                state = info[5]
                zipcody = info[6]
                classy = info[7]
                paymethod = info[8]
                pay_rates = [info[9], info[10], info[11]]
                routing = info[12]
                accounting = info[13]
                phone = info[14]
                ssn = info[15]
                dob = info[16]
                start = info[17]
                end = info[18]
                title = info[19]
                dept = info[20]
                archived = info[21]
                admin = info[22]
                # determine what class to instantiate for classy
                if classy == str(1):
                    classy = Salaried(info[9])  # Was 8, need to change to 9 to all these.. Off by 1 err
                elif classy == str(2):
                    classy = Commissioned(info[9], info[11])
                elif classy == str(3):
                    classy = Hourly(info[10])
                e = Employee(id_num, first, last, addy, city, state, zipcody, classy, paymethod, pay_rates, routing,
                             accounting, phone, ssn, dob, start, end, title, dept, archived, admin)  # instantiation
                total_employees.append(e)

                # IF NEW STARTUP AFTER SYSTEM_RESET.PY IT WILL SET THE DEFAULT PASSWORDS BACK TO LastFirstSSN format
                if e.get_password() == 'None':
                    e.set_default_password()


def process_timecards():
    '''Stores hours for each employee who works Hourly.'''
    timecards_file = os.path.dirname(__file__) + '\\HoursReports\\timecards.csv'
    with open(timecards_file, 'r') as f:
        data = f.readlines()
        for line in data:
            info = line.split(',')
            emp = find_employee_by_id(info[0])
            for num in info[1:]:
                if emp.classification == 'Hourly':
                    pay_stub = num.strip()
                    emp.classification.timecard.append(pay_stub)


def process_receipts():
    '''Stores receipts for each employee who works Commissioned.'''
    receipts_file = os.path.dirname(__file__) + '\\HoursReports\\receipts.csv'
    with open(receipts_file, 'r') as f:
        data = f.readlines()
        for line in data:
            info = line.split(',')
            emp = find_employee_by_id(info[0])
            if str(emp.classification) == 'Comissioned':
                for num in info[1:]:
                    emp.classification.receipts.append(num.strip())


def find_employee_by_id(id_number):
    '''Takes Employee id number as parameter. Returns Employee object from list with the
corresponding employee id.'''
    for e in total_employees:
        if e.emp_id == id_number:
            return e


def find_employee_by_partial_id(id_number):
    '''Takes any amount of id numbers you want and returns any employees that matches '''
    return_employees = []
    for e in total_employees:
        if e.emp_id.startswith(id_number):
            return_employees.append(e)
    return return_employees


def find_employee_by_last_name_filtered(last_name_entered, select_emp):
    '''Takes a last name or partial last name and filters through an already filtered list of employees'''
    return_employees = []
    last_name_entered = last_name_entered.upper()
    for e in select_emp:
        if e.last_name.startswith(last_name_entered):
            return_employees.append(e)
    return return_employees


def find_employee_by_last_name_total(last_name_entered):
    '''Takes a last name or partial last name and filters through all employees'''
    return_employees = []
    last_name_entered = last_name_entered.upper()
    for e in total_employees:
        if e.last_name.upper().startswith(last_name_entered):
            return_employees.append(e)
    return return_employees



def run_payroll():
    if os.path.exists(PAY_LOGFILE):  # pay_log_file is a global variable holding ‘payroll.txt’
        os.remove(PAY_LOGFILE)
    for emp in total_employees:  # employees is the global list of Employee objects
        emp.issue_pay(emp.classification.issue_payment())  # issue_payment calls a method in the classification
        # object to compute the pay


def main():
    load_employees()
    system.update_employee_file(total_employees)

    # Testing password functionality by changing everyones password to fart
    # load_employees()
    # for i in total_employees:
    #     print(i.get_password())
    # Remove if you want to test functionality and code

    # Testing the epic new code by setting a password to beansfartbananashit... Hella epik
    # Try it out, just remember to reset the database by running the restart_system.py file in the system folder <3
    # set_password('379767', 'beansfartbananashit')
    # get_password('379767')

    # Test original functionality of program

    # load_employees()
    # process_timecards()
    # process_receipts()
    # run_payroll()

    # # Change Karina Gay to Salaried and MailMethod by changing her Employee object:
    # emp = find_employee_by_id('688997')
    # emp.make_salaried(45884.99)
    # emp.issue_pay(emp.classification.issue_payment())
    # # Change TaShya Snow to Commissioned and DirectMethod; add some receipts
    # emp = find_employee_by_id('522759')
    # emp.make_commissioned(50005.50, 25)
    # clas = emp.classification
    # clas.add_receipts(1109.73)
    # clas.add_receipts(746.10)
    # emp.issue_pay(emp.classification.issue_payment())

    # # Change Rooney Alvarado to Hourly; add some hour entries
    # emp = find_employee_by_id('165966')
    # emp.make_hourly(21.53)
    # clas = emp.classification
    # clas.add_timecard(8.0)
    # clas.add_timecard(8.0)
    # clas.add_timecard(8.0)
    # clas.add_timecard(8.0)
    # clas.add_timecard(8.0)
    # emp.issue_pay(emp.classification.issue_payment())

