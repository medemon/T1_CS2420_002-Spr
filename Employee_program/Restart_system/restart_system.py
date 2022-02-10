import random
"""
Author: Nicolas Child
Class: CS2450-002
Team: 1
Description: Script that generates new database for payroll program
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
titles = ["Developer", "Senior Developer", "Data Scientist", "Janitor", "Cheeto Fetcher"]
def generate_title():
    return titles[random.randint(0, 4)]

departments = ["Low Level Design Department", "Digital design Department", "Statistics Department", "Management Department"]
def generate_department():
    return departments[random.randint(0, 3)]


def restart_system():
    """Function to add new values to employees.csv and restart the system if necessary"""
    lines = [] #Need a list of lines to save each individual line into when I separate them into lists by commas
    with open("employees.csv", 'r') as f:
        #Creating a list for all of the lines in the file
        lines_list = f.read().splitlines()
        for line_num in range(len(lines_list)):
            lines.append(lines_list[line_num].split(',')) #Separating lines into lists separated by commas
        lines.pop(0)
        #Removing descriptor section in the employees.csv file

        #Close out of file so it's not running in the background

    
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
        else:
            termination_date = None

        #Can use seggzy f string to save lots of space
        new_items = f"{generate_phone_number()},{generate_SSN()},{generate_DOB()},{generate_date()},{termination_date},{generate_title()},{generate_department()}"
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
    with open('employees_updated.csv', 'w') as f:
        f.write("ID,Name,Address,City,State,Zip,Classification,PayMethod,Salary,Hourly,Commission,Route,Account,Phone,SSN,DOB,Start_Date,End_Date,Title,Department\n")
        for line in lines:
            for item in range(len(line)):
                #Need to check if it is the last item in the list, if it is we don't want to end with a comma
                if item == (len(line) - 1):
                    f.write(line[item])
                else:
                    f.write(f"{line[item]},")
            #End each line with a newline
            f.write('\n')

    


def main():
    restart_system()

main()
