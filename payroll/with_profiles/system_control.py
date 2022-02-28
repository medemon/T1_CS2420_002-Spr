import random, os
"""
Author: Nicolas Child
Class: CS2450-002
Team: 1
Description: Script that generates new database for payroll program and password database blank
"""
random.seed(1)



# Random number generators w/ different lengths depending on how many random numbers needed
def four_random():
    return random.randint(1111,9999)
def three_random():
    return random.randint(111, 999)
def two_random():
    return random.randint(10, 99)

# Generates a random number using format 801-xxx-xxxx as integers
def generate_phone_number():
    return ("801" + '-' + str(three_random()) + '-' + str(four_random()))

#Generates random social security number
def generate_SSN():
    return (str(three_random()) + '-' + str(two_random()) + '-' + str(four_random()))

# Generates DOB formatted 1-12/1-28/64-99 (We only hire old pros lol)
def generate_DOB():
    return (str(random.randint(1, 12)) + '/' + str(random.randint(1, 28)) + '/' + str(random.randint(64, 99)))

# Generates start date (assume company founded in 2004) formatted (1-12/1-28/4-22)
# Can use the same function for the employees which we have fired we are assuming 75% 
# employees haven't been fired
def generate_date():
    # (str(random.randint(1, 12)) + '/' + str(random.randint(1, 28)) + '/' + str(random.randint(4, 22)))
    month = str(random.randint(1, 12))
    day = str(random.randint(1, 28))
    year = str(random.randint(4, 22))

    #Condition checks to make sure the zeros are padded
    if len(month) == 1:
        month = '0' + month

    if len(year) == 1:
        year = '0' + year

    return month + '/' + day + '/' + year

# Need to generate titles for all employees
def generate_title():
    titles = ["Supervisor", "Employee"]
    return titles[random.randint(0, 1)]

def generate_department():
    departments = ["Low Level Design Department", "Digital design Department", "Statistics Department"]
    return departments[random.randint(0, 2)]


def restart_system():
    """Function to add new values to employees.csv and restart the system if necessary. Also responsible
    for making the blank UN and PW database"""
    lines = [] #Need a list of lines to save each individual line into when I separate them into lists by commas
    employees_file = os.path.dirname(__file__) + '\\employees.csv'
    with open(employees_file, 'r') as f:
        #Creating a list for all of the lines in the file
        lines_list = f.read().splitlines()
        for line_num in range(len(lines_list)):
            lines.append(lines_list[line_num].split(',')) #Separating lines into lists separated by commas
        lines.pop(0)
        #Removing descriptor section in the employees.csv file

        #Close out of file so it's not running in the background

    #NOW We need to make it so that the names are also first name and last name.
    #So I am going to split up the 'name' part into first and last, save it
    #To a list, then when I am done with that I am going to append it to the lines
    #list and add it in.
        first_and_last_names_list = []
        for i in lines:
            #Some employees have first, m, last
            #NOT apart of the spec, so I am going to toss them out if they have a middle name.
            #Sorry bobbert
            first_and_last_and_middlenames_list = i[1].split(' ')
            if len(first_and_last_and_middlenames_list) == 3:
                first_and_last_and_middlenames_list.pop(1)
            first_and_last_names_list.append(first_and_last_and_middlenames_list)
        #Ugly but now we only have first names and last names
        #Now we need to remove the names part for each item in lines and add the first and last right there cuh
        
        #Now the simpliest way for me to do this would just be for me to override the name with the first name
        #Then simply insert the last name in the listeroo which is at index 1
    
        for emp in range(len(lines)):
            lines[emp][1] = first_and_last_names_list[emp][0]

        #Nice now that is done. Time to add the middle names into the list of lines

        for emp in range(len(lines)):
            lines[emp].insert(2, first_and_last_names_list[emp][1])

            

    #Now we need to append our new values to a list
    #Let's go ahead and loop through the list and add phone, SSN, DOB, start_date, end_date, title, department
    temp = []
    for line in lines:
        #Need to randomly assign a probability of 1/10 that an employee is terminated
        #If random number is 1, then employee no longer works at company, and termination date is filled
        #Else, it is assigned a value of None
        termination_factor = random.randint(1, 12)
        if termination_factor == 1:
            termination_date = generate_date()
            archived = 1
        else:
            termination_date = None
            archived = 0

        #Can use seggzy f string to save lots of space
        new_items = f"{generate_phone_number()},{generate_SSN()},{generate_DOB()},{generate_date()},{termination_date},{generate_title()},{generate_department()},{archived},{random.randint(0, 1)}"
        #Now we are going to change variable to list and split by commas
        new_items = new_items.split(',')
        #Now it's just concatinating our lines list with our new_items list
        line = line + new_items
        temp.append(line)
    lines = []
    #Updating old lines list with newly updated items
    lines = temp

    #With this exact seed and setup there is exactly one employee terminated --> bueno

    #OK time to make a new file for our updated employees and their items

    #ID,Name,Address,City,State,Zip,Classification,PayMethod,Salary,Hourly,Commission,Route,Account,Phone,SSN,DOB,start_date,end_date,title,department
    new_employees_file = os.path.dirname(__file__) + '\\employees_updated.csv'
    with open(new_employees_file, 'w') as f:
        f.write("ID,first,last,Address,City,State,Zip,Classification,PayMethod,Salary,Hourly,Commission,Route,Account,Phone,SSN,DOB,Start_Date,End_Date,Title,Department,Archived,Admin\n")
        for line in lines:
            for item in range(len(line)):
                #Need to check if it is the last item in the list, if it is we don't want to end with a comma
                if item == (len(line) - 1):
                    f.write(line[item])
                else:
                    f.write(f"{line[item]},")
            #End each line with a newline
            f.write('\n')

    #Now we need to create blank password file
    new_password_file = os.path.dirname(__file__) + '\\passwords.csv'
    with open(new_password_file, 'w') as f:
        #Template line for the file
        f.write(f"Username, Password\n")
        for i in range(len(lines)):
            f.write(f"{lines[i][0]},None\n")


def update_employee_file(emp_list):
    """Function that takes the loaded employee list and updates the employees_updated file.. should be updated_updated, jk"""
    #Okay so we need to scan each individual employee and write their data in the format of
    #ID, first, last, address, city, state, zip, classification, paymentMethod, salary, hourly, comission, routingNum, AccountingNum
    #phone, SSN, DOB, startDate, endDate, title, dept

    new_employees_file = os.path.dirname(__file__) + '\\employees_updated.csv'
    with open(new_employees_file, 'w') as f:
        f.write("ID,first,last,address,city,state,zip,classification,paymentmethod,salary,hourly,commission,routing,AccountingNum")
        f.write("phone,SSN,DOB,startDate,endDate,title,dept,Archived,Admin\n")
        for employee in emp_list:
            f.write(f"{employee.emp_id},{employee.first_name},{employee.last_name},{employee.address},{employee.city},{employee.state},{employee.zipcode},{int(employee.classification)},")
            f.write(f"{employee.payment_method},{employee.pay_rates[0]},{employee.pay_rates[1]},{employee.pay_rates[2]},{employee.route},{employee.accounting},{employee.phone},")
            f.write(f"{employee.SSN},{employee.DOB},{employee.start_date},{employee.end_date},{employee.title},{employee.dept},{employee.archived},{employee.admin}")
    #VALIDATION CODE TO MAKE SURE FILES MATCH

def main():
    restart_system()

if __name__ == "__main__":
    main()