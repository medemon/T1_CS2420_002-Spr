import os, os.path, shutil
from abc import ABC, abstractmethod
employees = []
hours = {}
receipts = {}
PAY_LOGFILE = "paylog.txt"

class Employee:
    def __init__(self, ID, first_name, last_name, address, city, state, zipp, num):
        self.ID = ID
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.state = state
        self.zip = zipp
        self.num = num
        # Hourly = 3, comissioned = 2, salary = 1
    def make_hourly(self, pay):
        self.hourly = pay
        self.num = 3
        if self.ID not in hours:
            hours[f"{self.ID}"] = []
        self.classification = Hourly(self.ID)
        
    def make_salaried(self, pay):
        self.salary = pay
        self.num = 1
        self.classification = Salaried()

    def make_comissioned(self, pay, percent):
        self.salary = pay
        self.comission = percent
        self.num = 2
        if self.ID not in receipts:
            receipts[f"{self.ID}"] = []
        self.classification = Comissioned(self.ID)

    def issue_payment(self):
        payment = Classification.classification_checker(self, self)
        payroll = round(payment, 2)
        if self.num == 3:
            hours[f"{self.ID}"] = []
        if self.num == 2:
            receipts[f"{self.ID}"] = []
        if int(payroll) == 0:
            pass
        else:
            with open("paylog.txt", 'a+') as f:
                f.write(f"""Mailing {payroll} to {self.first_name} {self.last_name} at {self.address} {self.city} {self.state} {self.zip}\n""")
        return payroll

def load_employees():
    global employees
    with open("employees.csv", 'r') as f:
        count = 0
        for lines in f:
            count += 1
            if count == 1:
                pass
            else:
                items = lines.split(',')
                no_new_line = items[-1].strip("\n")
                items[-1] = no_new_line
                employee_instance = Employee(items[0], items[1], items[2], items[3], items[4], items[5], items[6], items[7])
                employees.append(employee_instance)
                if items[7] == str(3):
                    employee_instance.make_hourly(items[10])
                if items[7] == str(1):
                    employee_instance.make_salaried(items[8])
                if items[7] == str(2):
                    employee_instance.make_comissioned(items[8], items[9])

class Classification(ABC):
    @abstractmethod
    def issue_pay(self, pay):
        pass
    def classification_checker(self, emp_instance):
        employee = emp_instance
        if employee.num == 3:
            return Hourly.issue_pay(self, employee.ID, employee.hourly)
        if employee.num == 1:
            return Salaried.issue_pay(self, employee.salary)
        if employee.num == 2:
            return Comissioned.issue_pay(self, employee.comission, employee.salary, employee.ID)

class Hourly(Classification):
    def __init__(self, id):
        self.id = id
    def issue_pay(self, id, pay):
        money = 0
        hours_list = hours[id]
        for stuff in hours_list:
            money += (float(stuff) * float(pay))
        return money
    def add_timecard(self, time):
        hour_list = hours[f'{self.id}']
        hour_list.append(time)
        # Makes it so that new id's can be added to dictionary if not present.
        hours[f'{self.id}'] = hour_list

class Salaried(Classification):
    def issue_pay(self, pay):
        return ((1/24) * float(pay))
    

class Comissioned(Salaried):
    def __init__(self, id):
        self.identification = id
    def issue_pay(self, rate, pay, id):
        salary = Salaried.issue_pay(self, pay)
        receipt_list = receipts[id]
        comission_total = 0
        for items in receipt_list:
            comission_total += float(items)
        comission = comission_total * (float(rate)/ 100)
        return comission + salary
    def add_receipt(self, amount):
        receipt_list = receipts[self.identification]
        receipt_list.append(amount)
        receipts[self.identification] = receipt_list

def process_timecards():
    with open("timecards.csv", 'r') as f:
        for line in f:
            lines = line.split(',')
            no_new_line = lines[-1].strip('\n')
            lines[-1] = no_new_line
            lines = list(filter(None, lines)) 
            hours[f"{lines[0]}"] = list(lines[1:])
        with open("timecards.txt", 'w+') as s:
            s.write(f.read())
def process_receipts():
    with open("receipts.csv", 'r') as f:
        for line in f:
            lines = line.split(',')
            no_new_line = lines[-1].strip('\n')
            lines[-1] = no_new_line
            receipts[f"{lines[0]}"] = list(lines[1:])
def find_employee_by_id(ID):
    for x in range(len(employees)):
        if ID == employees[x].ID:
            return employees[x]
def run_payroll():
    if os.path.exists(PAY_LOGFILE): 
        os.remove(PAY_LOGFILE)
    for emp in employees: 
        emp.issue_payment() 
