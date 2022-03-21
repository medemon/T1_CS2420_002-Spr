from tkinter import simpledialog
from payroll import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image

import os, os.path


class Window(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Admin Status
        self.admin = BooleanVar()
        self.admin.set(True)
        # User ID
        self.user_id = ''
        # Chosen Employee if viewing information
        self.chosen_employee = ''
        # Styles so the Windows look slightly more appealing
        style = ttk.Style(self)

        self.tk.call('source', os.path.dirname(__file__) + '\\Forest-ttk-theme-master\\forest-dark.tcl')

        style.theme_use('forest-dark')

        # Title
        self.title("Employee Management System")

        # Sets the Size of the Window and the Frame
        self.geometry("1000x700")
        container = Frame(self)

        self.iconbitmap(os.path.dirname(__file__) + '\\images\\window_icon.ico')

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Starts up the List of Screens
        self.screens = {}
        # This is the list of classes that it runs through, generates a frame for, then Appends into the Screens list
        for F in (Login_Screen, Employee_Profile_Screen, Reports_Screen, Search_Screen, Employee_Payroll_Screen):
            frame = F(container, self)

            self.screens[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        # Defaults Screen
        self.show_frame(Login_Screen)

    # Called when Switching Frames or Screens
    def show_frame(self, cont, arg=NONE):
        if self.user_id != '':
            self.check_admin()
        frame = self.screens[cont]
        frame.tkraise()
        if arg == NONE:
            pass
        else:
            frame.initiate(self, arg)

    # Checks the Admin status of the current user
    def check_admin(self):
        temp = find_employee_by_id(self.user_id)
        if int(temp.admin) == 1:
            self.admin.set(True)
        else:
            self.admin.set(False)

    # Changes the Variable for the Selected Employee
    def select_employee(self, id):
        self.chosen_employee = id
        self.show_frame(Employee_Profile_Screen, id)


class Login_Screen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        print("Logging In")

        self.id_label = Label(self, text="User Name", fg="green", font=("Tahoma", 14))
        self.id_box = Entry(self, width=25, font="Tahoma")

        self.pw_label = Label(self, text="Password", fg="green", font=("Tahoma", 14))
        self.p_box = Entry(self, width=25, font="Tahoma", show="*")

        self.submit_button = Button(self, text="Login", command=lambda: self.retrieve_login(controller))

        # Packs all of the Widgets for the screen
        self.id_label.pack()
        self.id_box.pack()

        self.pw_label.pack()
        self.p_box.pack()

        self.submit_button.pack()

    def retrieve_login(self, controller):
        id_value = self.id_box.get()
        pw_value = self.p_box.get()
        print("\nEntered Employee ID: " + id_value)
        print("Entered Password: " + pw_value)

        print("\nHere is a test Employee ID: " + total_employees[0].emp_id)
        # Add way to save UserName  with chosen_user
        for x in total_employees:
            if x.emp_id == id_value:
                print("\nHere is the user's password: " + get_password(id_value))
                chosen_user = id_value
                if get_password(id_value) == pw_value:
                    print("Successfully Logged In")
                    self.login_success(controller, id_value)
                else:
                    print("Incorrect Password")

    def login_success(self, controller, id):
        controller.user_id = self.id_box.get()
        controller.select_employee(controller.user_id)


class Employee_Profile_Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Creates the Logo Image on the Page
        img = Image.open(os.path.dirname(__file__) + '\\images\\Logo.png')
        icon_image = ImageTk.PhotoImage(img)
        self.logo_label = Label(self, width=300, height=175, image=icon_image)
        self.logo_label.image = icon_image
        self.logo_label.place(y=45, x=5)
        # Employee Profle Screen Title
        self.title_label = Label(self, text="Employee Profile Screen", fg="green",
                                font=("Tahoma", 18, "underline", "bold"))
        self.title_label.place(height=50, width=300)

        # Frame for displaying profile information
        self.profile_screen = Frame(self, height=600, width=690, bg="gray")
        self.profile_screen.place(x=300, y=10)

        # Employee object
        self.employee = object

        # Labels for current Employee ID and infromation
        self.emp_id = StringVar()
        self.arch = StringVar()
        self.mode = StringVar()
        self.desc_label = Label(self, text="Currently viewing ID:", font=("Tahma", 13))
        self.desc_label.place(x=150, y=250, anchor=CENTER)
        self.id_label = Label(self, textvariable=self.emp_id, font=("Tahma", 13))
        self.id_label.place(x=150, y=270, anchor=CENTER)
        self.arch_label = Label(self, textvariable=self.arch, font=("Tahma", 13))
        self.arch_label.place(x=150, y=290, anchor=CENTER)
        self.mode_label = Label(self, textvariable=self.mode, font=("Tahma", 13))
        self.mode_label.place(x=150, y=350, anchor=CENTER)

        # Profile labels, entry fields
        self.first_name = StringVar()
        self.first_name_label = Label(self.profile_screen, text="First Name:", bg="grey", font=("Tahoma", 13))
        self.first_name_entry = Entry(self.profile_screen, bd=1, width=75, textvariable=self.first_name)
        self.first_name_label.place(x=10, y=50)
        self.first_name_entry.place(x=120, y=50)
        self.last_name = StringVar()
        self.last_name_label = Label(self.profile_screen, text="Last Name:", bg="grey", font=("Tahoma", 13))
        self.last_name_entry = Entry(self.profile_screen, bd=1, width=75, textvariable=self.last_name)
        self.last_name_label.place(x=10, y=90)
        self.last_name_entry.place(x=120, y=90)
        self.address = StringVar()
        self.address_label = Label(self.profile_screen, text="Address:", bg="grey", font=("Tahoma", 13))
        self.address_entry = Entry(self.profile_screen, bd=1, width=75, textvariable=self.address)
        self.address_label.place(x=10, y=130)
        self.address_entry.place(x=120, y=130)
        self.city = StringVar()
        self.city_label = Label(self.profile_screen, text="City:", bg="grey", font=("Tahoma", 13))
        self.city_entry = Entry(self.profile_screen, bd=1, width=75, textvariable=self.city)
        self.city_label.place(x=10, y=170)
        self.city_entry.place(x=120, y=170)
        self.state = StringVar()
        self.state_label = Label(self.profile_screen, text="State:", bg="grey", font=("Tahoma", 13))
        self.state_entry = Entry(self.profile_screen, bd=1, width=75, textvariable=self.state)
        self.state_label.place(x=10, y=210)
        self.state_entry.place(x=120, y=210)
        self.zip = StringVar()
        self.zip_label = Label(self.profile_screen, text="Zipcode:", bg="grey", font=("Tahoma", 13))
        self.zip_entry = Entry(self.profile_screen, bd=1, width=75, textvariable=self.zip)
        self.zip_label.place(x=10, y=250)
        self.zip_entry.place(x=120, y=250)
        self.phone = StringVar()
        self.phone_label = Label(self.profile_screen, text="Phone:", bg="grey", font=("Tahoma", 13))
        self.phone_entry = Entry(self.profile_screen, bd=1, width=75, textvariable=self.phone)
        self.phone_label.place(x=10, y=290)
        self.phone_entry.place(x=120, y=290)
        self.dob = StringVar()
        self.dob_label = Label(self.profile_screen, text="DOB:", bg="grey", font=("Tahoma", 13))
        self.dob_entry = Entry(self.profile_screen, bd=1, width=75, textvariable=self.dob)
        self.dob_label.place(x=10, y=330)
        self.dob_entry.place(x=120, y=330)
        self.dept = StringVar()
        self.dept_label = Label(self.profile_screen, text="Department:", bg="grey", font=("Tahoma", 13))
        self.dept_entry = Entry(self.profile_screen, bd=1, width=75, textvariable=self.dept)
        self.dept_label.place(x=10, y=370)
        self.dept_entry.place(x=120, y=370)
        self.title = StringVar()
        self.title_label = Label(self.profile_screen, text="Title:", bg="grey", font=("Tahoma", 13))
        self.title_entry = Entry(self.profile_screen, bd=1, width=75, textvariable=self.title)
        self.title_label.place(x=10, y=410)
        self.title_entry.place(x=120, y=410)
        self.start_date = StringVar()
        self.start_date_label = Label(self.profile_screen, text="Start Date:", bg="grey", font=("Tahoma", 13))
        self.start_date_entry = Entry(self.profile_screen, bd=1, width=75, textvariable=self.start_date)
        self.start_date_label.place(x=10, y=450)
        self.start_date_entry.place(x=120, y=450)
        self.end_date = StringVar()
        self.end_date_label = Label(self.profile_screen, text="End Date:", bg="grey", font=("Tahoma", 13))
        self.end_date_entry = Entry(self.profile_screen, bd=1, width=75, textvariable=self.end_date)
        self.end_date_label.place(x=10, y=490)
        self.end_date_entry.place(x=120, y=490)
        self.archived = BooleanVar()
        self.archived_checkbox = Checkbutton(self.profile_screen, text="Archived", bg='grey', selectcolor='black', variable=self.archived, font=("Tahoma", 13))
        self.archived_checkbox.place(x=10, y=530)
        self.is_admin = BooleanVar()
        self.admin_checkbox = Checkbutton(self.profile_screen, text="Admin", bg='grey', selectcolor='black', variable=self.is_admin, font=("Tahoma", 13))
        self.admin_checkbox.place(x=100, y=530)

        # Save Button
        self.save_button = Button(self, text="Save", width=7, bg="grey", font=("Tahoma", 10, "bold"),
                                    command=lambda: self.save(controller)
                                    )
        self.save_button.place(x=150, y=380, anchor=CENTER)

        # Password Diaplog Button
        self.payroll_button = Button(self, text="Change Password", width=14, bg="grey", font=("Tahoma", 10, "bold"),
                                    command=lambda: self.new_password_dialog(controller))
        self.payroll_button.place(x=150, y=420, anchor=CENTER)

        # Payroll Screen Button
        self.payroll_button = Button(self, text="Employee payroll", width=14, bg="grey", font=("Tahoma", 10, "bold"),
                                    command=lambda: controller.show_frame(Employee_Payroll_Screen, controller.chosen_employee))
        self.payroll_button.place(x=150, y=460, anchor=CENTER)

        # Search Screen Button
        self.search_button = Button(self, text="Search Screen", width=14, bg="grey", font=("Tahoma", 10, "bold"),
                                    command=lambda: controller.show_frame(Search_Screen))
        self.search_button.place(x=150, y=500, anchor=CENTER)

    def initiate(self, controller, id):
        '''For the Employee_Profile_Screen this method will check the permissions of the logged in user to determine what they are allowed to edit
        and populates the entry box with data from the given id's employee object'''

        # If id is 0 then starts a new employee with a randomly generated ID.
        if id == '0':
            new_id = str(system.four_random()) + str(system.two_random())
            while find_employee_by_id(new_id) != None:
                new_id = system.four_random() + system.two_random()
            self.emp_id.set(new_id)
            self.arch.set("Enter New Employee")
            self.employee = None
            self.payroll_button.config(state='disabled')
            return        

        # Run permissions check
        user_access = [self.address_entry,self.state_entry,self.city_entry,self.zip_entry,self.phone_entry]
        admin_access = [self.first_name_entry,self.last_name_entry,self.dob_entry,self.dept_entry,self.title_entry,self.start_date_entry,self.end_date_entry]
        # Always sets all Entry to disable first to avoid fields remaining open when switching viewed profiles.
        for i in user_access:
            i.config(state = 'disabled', disabledbackground="grey", disabledforeground='white')
        for i in admin_access:
            i.config(state = 'disabled', disabledbackground="grey", disabledforeground='white')
        self.payroll_button.config(state='disabled')
        self.archived_checkbox.config(state='disabled')
        self.admin_checkbox.config(state='disabled')
        self.mode.set("Read-only Mode")
        # Owned account access
        if controller.user_id == id or controller.admin.get():
            for i in user_access:
                i.config(state = 'normal', bg="white", fg="black")
            self.payroll_button.config(state='normal')
            self.mode.set("User Edit Mode")
        # Admin access
        if controller.admin.get():
            for i in admin_access:
                i.config(state = 'normal', bg="white", fg="black")
            self.archived_checkbox.config(state='normal')
            self.admin_checkbox.config(state='normal')
            self.mode.set("Admin Mode")
        # Populate fields
        self.employee = find_employee_by_id(id)
        self.first_name.set(self.employee.first_name)
        self.last_name.set(self.employee.last_name)
        self.address.set(self.employee.address)
        self.city.set(self.employee.city)
        self.state.set(self.employee.state)
        self.zip.set(self.employee.zipcode)
        self.phone.set(self.employee.phone)
        self.dob.set(self.employee.DOB)
        self.dept.set(self.employee.dept)
        self.title.set(self.employee.title)
        self.start_date.set(self.employee.start_date)
        self.end_date.set(self.employee.end_date)
        self.emp_id.set(self.employee.emp_id)
        self.archived.set(int(self.employee.archived))
        self.is_admin.set(int(self.employee.admin))
        if self.employee.archived == True:
            self.arch.set("Employee is INACTIVE")
        else:
            self.arch.set("Employee is ACTIVE")
        self.first_time_check(controller)

    def save(self, controller):
            '''Saves all entered data to the employee object ~EXPAND ON THIS LATER, NEEDS CHECKS FOR TRASH ENTRIES!~'''
            query = messagebox.askquestion('save','save changes?')
            if query == 'yes':
                if self.employee != None:
                    self.employee.first_name = self.first_name.get()
                    self.employee.last_name =self.last_name.get()
                    self.employee.address = self.address.get()
                    self.employee.city = self.city.get()
                    self.employee.state = self.state.get()
                    self.employee.zipcode = self.zip.get()
                    self.employee.phone = self.phone.get()
                    self.employee.DOB = self.dob.get()
                    self.employee.dept = self.dept.get()
                    self.employee.title = self.title.get()
                    self.employee.start_date = self.start_date.get()
                    self.employee.end_date = self.end_date.get()
                    self.employee.archive_employee(self.archived.get())
                    self.employee.set_admin(self.is_admin.get())
                    messagebox.showinfo("Message", "Save Successful!")
                else:
                    new_list = [self.emp_id.get(),self.first_name.get(),self.last_name.get(),self.address.get(),self.city.get(),self.state.get(),self.zip.get(),self.phone.get(),
                                self.dob.get(),self.dept.get(),self.title.get(),self.start_date.get(),self.end_date.get(),self.archived.get(),self.is_admin.get()]
                    messagebox.showinfo("Message", "Please continue on payroll screen")
                    controller.show_frame(Employee_Payroll_Screen, new_list)
            else:
                pass

    def new_password_dialog(self, controller):
        '''Upon User selecting new password, this method will raise a simple dialog box for them to enter the new password'''
        messagebox.showinfo("Message", "Your password is set to default and needs to change!")
        query = simpledialog.askstring("New Password", "Enter New Password.", show="*")
        if query != None:
            set_password(controller.chosen_employee, query)
            messagebox.showinfo("Message", "Password updated!")
        else:
            messagebox.showinfo("Message", "Password not changed!")

    def first_time_check(self, controller):
        '''This method checks if the employee passwors is at its default for first time users, so it will bring up the new password prompt'''
        default = f"{self.employee.last_name}{self.employee.first_name}{self.employee.SSN[-4:]}"
        if self.employee.get_password() ==  default and controller.user_id == self.employee.emp_id:
            self.new_password_dialog(controller)

class Reports_Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.title_label = Label(self, text="Paylog Report", fg="green", font=("Tahoma", 20, "underline"))
        self.emp_profile_button = Button(self, text="Return to Search Screen",
                                         command=lambda: controller.show_frame(Search_Screen))
        self.title_label.pack()
        self.emp_profile_button.place(x=10, y=650)

        f = open(os.path.dirname(__file__) + "\\HoursReports\\paylog.txt", "r")
        yloc = 50
        xloc = 0
        for x in f:
            Label(self, text=x, fg="green", font=("Tahoma", 8)).place(x=xloc, y=yloc)
            yloc += 25
            if yloc >= 625:
                xloc += 500
                yloc = 50

    pass


class Employee_Payroll_Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Creates the Logo Image on the Page
        img = Image.open(os.path.dirname(__file__) + '\\images\\Logo.png')
        icon_image = ImageTk.PhotoImage(img)
        self.logo_label = Label(self, width=300, height=175, image=icon_image)
        self.logo_label.image = icon_image
        self.logo_label.place(y=45, x=5)
        # Employee Payroll Screen Title
        self.title_label = Label(self, text="Employee Payroll Screen", fg="green",
                                font=("Tahoma", 18, "underline", "bold"))
        self.title_label.place(height=50, width=300)

        # Frame for displaying profile information
        self.profile_screen = Frame(self, height=600, width=690, bg="gray")
        self.profile_screen.place(x=300, y=10)

        # Employee object
        self.employee = object

        # New Employee List
        self.new_list = None

        # Labels for current Employee ID and infromation
        self.emp_id = StringVar()
        self.arch = StringVar()
        self.mode = StringVar()
        self.desc_label = Label(self, text="Currently viewing ID:", font=("Tahma", 13))
        self.desc_label.place(x=150, y=250, anchor=CENTER)
        self.id_label = Label(self, textvariable=self.emp_id, font=("Tahma", 13))
        self.id_label.place(x=150, y=270, anchor=CENTER)
        self.arch_label = Label(self, textvariable=self.arch, font=("Tahma", 13))
        self.arch_label.place(x=150, y=290, anchor=CENTER)
        self.mode_label = Label(self, textvariable=self.mode, font=("Tahma", 13))
        self.mode_label.place(x=150, y=350, anchor=CENTER)

        # Pay related labels, entry fields
        self.ssn = StringVar()
        self.ssn_label = Label(self.profile_screen, text="SSN:", bg="grey", font=("Tahoma", 13))
        self.ssn_entry = Entry(self.profile_screen, bd=1, width=70, textvariable=self.ssn)
        self.ssn_label.place(x=10, y=170)
        self.ssn_entry.place(x=150, y=170)
        self.classy_opts = ['Salaried','Commissioned','Hourly']
        self.classy = StringVar()
        self.classy_label = Label(self.profile_screen, text="classification:", bg="grey", font=("Tahoma", 13))
        self.classy_drop = OptionMenu(self.profile_screen, self.classy, *self.classy_opts)
        self.classy_drop.config(bg="grey", font=("Tahoma", 13))
        self.classy_label.place(x=10, y=210)
        self.classy_drop.place(x=150, y=210)
        self.salary = StringVar()
        self.salary_label = Label(self.profile_screen, text="Salary:", bg="grey", font=("Tahoma", 13))
        self.salary_entry = Entry(self.profile_screen, bd=1, width=70, textvariable=self.salary)
        self.salary_label.place(x=10, y=250)
        self.salary_entry.place(x=150, y=250)
        self.rate = StringVar()
        self.rate_label = Label(self.profile_screen, text="Rate:", bg="grey", font=("Tahoma", 13))
        self.rate_entry = Entry(self.profile_screen, bd=1, width=70, textvariable=self.rate)
        self.rate_label.place(x=10, y=290)
        self.rate_entry.place(x=150, y=290)
        self.meth_opts = ['Direct Deposit', 'Mailed']
        self.pay_method = StringVar()
        self.pay_method_label = Label(self.profile_screen, text="Payment Method:", bg="grey", font=("Tahoma", 13))
        self.pay_method_drop = OptionMenu(self.profile_screen, self.pay_method, *self.meth_opts)
        self.pay_method_drop.config(bg="grey", font=("Tahoma", 13))
        self.pay_method_label.place(x=10, y=330)
        self.pay_method_drop.place(x=150, y=330)
        self.routing = StringVar()
        self.routing_label = Label(self.profile_screen, text="Route Number:", bg="grey", font=("Tahoma", 13))
        self.routing_entry = Entry(self.profile_screen, bd=1, width=70, textvariable=self.routing)
        self.routing_label.place(x=10, y=370)
        self.routing_entry.place(x=150, y=370)
        self.account = StringVar()
        self.account_label = Label(self.profile_screen, text="Account Number:", bg="grey", font=("Tahoma", 13))
        self.account_entry = Entry(self.profile_screen, bd=1, width=70, textvariable=self.account)
        self.account_label.place(x=10, y=410)
        self.account_entry.place(x=150, y=410)

        # Receipt Button
        self.receipt_button = Button(self.profile_screen, text="Add Receipt", width=14, bg="grey", font=("Tahoma", 10, "bold"),
                                    command=lambda: self.add_receipt_diag()
                                    )
        self.receipt_button.place(x=10, y=490)

        # Save Button
        self.save_button = Button(self, text="Save", width=7, bg="grey", font=("Tahoma", 10, "bold"),
                                    command=lambda: self.save(controller)
                                    )
        self.save_button.place(x=150, y=380, anchor=CENTER)

        # Profile Screen Button
        self.profile_button = Button(self, text="Employee Profile", width=14, bg="grey", font=("Tahoma", 10, "bold"),
                                    command=lambda: controller.show_frame(Employee_Profile_Screen, controller.chosen_employee))
        self.profile_button.place(x=150, y=420, anchor=CENTER)

        # Search Screen Button
        self.search_button = Button(self, text="Search Screen", width=14, bg="grey", font=("Tahoma", 10, "bold"),
                                    command=lambda: controller.show_frame(Search_Screen))
        self.search_button.place(x=150, y=460, anchor=CENTER)

    def initiate(self, controller, arg):
        '''For the Employee_Payroll_Screen this method will check the permissions of the logged in user to determine what they are allowed to edit
        and populates the entry box with data from the given id's employee object'''

        # If there is a list, it is a new employee, leaves entries blank and open
        if isinstance(arg,list):
             self.arch.set("Enter New Employee")
             self.new_list = arg
             self.receipt_button.config(state='disable')
             return
        # Run permissions check
        user_access = [self.routing_entry,self.account_entry]
        admin_access = [self.salary_entry,self.rate_entry,self.ssn_entry]
        # Always sets all Entry to disable first to avoid fields remaining open when switching viewed profiles.
        for i in user_access:
            i.config(state='disabled', disabledbackground='grey', disabledforeground='white')
        for i in admin_access:
            i.config(state='disabled', disabledbackground='grey', disabledforeground='white')
        self.classy_drop.config(state='disabled')
        self.pay_method_drop.config(state='disabled')
        self.receipt_button.config(state='disabled')
        self.mode.set("Read-only Mode")
        # Owned account access
        if controller.user_id == arg or controller.admin.get():
            for i in user_access:
                i.config(state='normal', bg='white', fg='black')
            self.pay_method_drop.config(state='normal')
            self.mode.set("User-Edit Mode")
        # Admin access
        if controller.admin.get():
            for i in admin_access:
                i.config(state='normal', bg='white', fg='black')
            self.classy_drop.config(state='normal')
            self.mode.set("Admin Mode")
        # Populate fields
        self.employee = find_employee_by_id(arg)
        self.classy.set(self.employee.classification)
        if self.employee.payment_method == '2':
            self.pay_method.set("Direct Deposit")
        else:
            self.pay_method.set("Mailed")
        if int(self.employee.classification) == 1:
            self.salary.set(self.employee.pay_rates[0])
            self.rate_entry.config(state='disabled', disabledbackground='grey', disabledforeground='white')
        elif int(self.employee.classification) == 2:
            self.salary.set(self.employee.pay_rates[0])
            self.rate.set(self.employee.pay_rates[1])
            self.receipt_button.config(state='normal')
        elif int(self.employee.classification) == 3:
            self.rate.set(self.employee.pay_rates[2])
            self.salary_entry.config(state='disabled', disabledbackground='grey', disabledforeground='white')
        self.routing.set(self.employee.route)
        self.account.set(self.employee.accounting)
        self.emp_id.set(self.employee.emp_id)
        self.ssn.set(self.employee.SSN)
        if self.employee.archived == True:
            self.arch.set("Employee is INACTIVE")
        else:
            self.arch.set("Employee is ACTIVE")

    def save(self,controller):
            '''Saves all entered data to the employee object ~EXPAND ON THIS LATER, NEEDS CHECKS FOR TRASH ENTRIES!~'''
            # If there is a list, it is a new Employee, uses the new Employee save
            if self.new_list != None:
                salary = 0
                comm = 0
                hourly = 0 
                if self.classy.get() == 'Salaried':
                    self.classy.set(1)
                    salary = self.salary.get()
                elif self.classy.get() == 'Commissioned':
                    self.classy.set(2)
                    salary = self.salary.get()
                    comm = self.rate.get()
                elif self.classy.get() == 'Hourly':
                    self.classy.set(3)
                    comm = self.rate.get()
                if self.pay_method.get() == 'Direct Deposit':
                    self.pay_method.set(2)
                else:
                     self.pay_method.set(1)
                add = [self.classy.get(),[salary,comm,hourly],self.pay_method.get(),self.routing.get(),self.account.get(),self.ssn.get()]
                self.new_list.extend(add)
                e = Employee(self.new_list[0], self.new_list[2], self.new_list[1], self.new_list[3], self.new_list[4], self.new_list[5], self.new_list[6], 
                             self.new_list[15], self.new_list[17], self.new_list[16], self.new_list[18],self.new_list[19], self.new_list[7], self.new_list[20], 
                             self.new_list[8], self.new_list[11], self.new_list[12], self.new_list[10], self.new_list[9], self.new_list[13], self.new_list[14])
                total_employees.append(e)
                e.set_default_password()
                controller.select_employee(e.emp_id)
                messagebox.showinfo("Message", "New Employee Added!")
                return

            query = messagebox.askquestion('save','save changes?')
            if query == 'yes':
                if self.classy.get() == 'Salaried':
                    if self.salary.get() != "":
                        self.employee.pay_rates[0] = self.salary.get()
                    self.employee.classification = Salaried(self.employee.pay_rates[0])
                elif self.classy.get() == 'Commissioned':
                    if self.salary.get() != "":
                        self.employee.pay_rates[0] = self.salary.get()
                    if self.rate.get() != "":
                        self.employee.pay_rates[1] = self.rate.get()
                    self.employee.classification = Commissioned(self.employee.pay_rates[0],self.employee.pay_rates[1])
                elif self.classy.get() == 'Hourly':
                    if self.rate.get() != "":
                        self.employee.pay_rates[2] = self.rate.get()
                    self.employee.classification = Hourly(self.employee.pay_rates[2])
                if self.pay_method.get() == 'Direct Deposit':
                    self.employee.payment_method = 2
                else:
                    self.employee.payment_method = 1
                self.employee.route = self.routing.get()
                self.employee.accounting = self.account.get()
                self.employee.SSN = self.ssn.get()
                messagebox.showinfo("Message", "Save Successful!")
            else:
                pass

    def add_receipt_diag(self):
        '''Upon User selecting add recept, this method will raise a simple dialog box for them to enter the amount'''
        query = simpledialog.askstring("Update Reciepts", "Enter receipt amount.")
        self.employee.classification.add_receipt(query)
        messagebox.showinfo("Message", "Reciepts updated!")



class Search_Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Creates the Logo Image on the Page
        img = Image.open(os.path.dirname(__file__) + '\\images\\Logo.png')
        icon_image = ImageTk.PhotoImage(img)
        self.logo_label = Label(self, width=300, height=175, image=icon_image)
        self.logo_label.image = icon_image
        self.logo_label.place(y=45, x=5)
        # Search Screen Title
        self.title_label = Label(self, text="Employee Search Screen", fg="green",
                                 font=("Tahoma", 18, "underline", "bold"))
        self.title_label.place(height=50, width=300)

        # Last Name Search Widget and Label
        self.last_name_label = Label(self, text="Last Name", font=("Tahoma", 13))
        self.last_name_entry = Entry(self, bd=1, bg="grey")
        self.last_name_label.place(x=10, y=200)
        self.last_name_entry.place(x=10, y=230)

        # Employee ID Search Widget and Label
        self.ID_label = Label(self, text="Employee ID", font=("Tahoma", 12))
        self.ID_entry = Entry(self, bd=1, bg="grey")
        self.ID_label.place(x=10, y=300)
        self.ID_entry.place(x=10, y=330)

        # Frame for displaying all results
        self.results_screen = Frame(self, height=600, width=690, bg="gray")
        self.results_screen.place(x=300, y=10)

        # Search Button
        self.search_button = Button(self, text="Search", width=7, bg="grey", font=("Tahoma", 10, "bold"),
                                    command=lambda: self.display_results(self.results_screen, controller)
                                    )
        self.search_button.place(x=125, y=380)

        # New Employee Button and changes selected employee to 0
        self.new_employee_button = Button(self, text="Add Employee", width=12, bg="grey", font=("Tahoma", 10, "bold"),
                                          command=lambda: controller.select_employee('0'))
        
        # Report Button
        self.report_button = Button(self, text="Reports Screen",
                                    command=lambda: controller.show_frame(Reports_Screen))
        # Runs an Admin Check
        if controller.admin.get():
            self.new_employee_button.place(x=15, y=450)
            self.report_button.place(x=185, y=450)

    # Called upon Searching to populate fields
    def display_results(self, results_screen, controller):
        self.clear_widgets(results_screen)
        # Gets the entered Search values
        id_entered = False
        retrieved_employees = []
        get_ID = self.ID_entry.get()
        get_last_name = self.last_name_entry.get()

        # Checks the ID and if entered filters through all ID's
        if get_ID == '':
            print("No ID Entered")
        else:
            id_entered = True
            print("ID: " + get_ID)
            retrieved_employees = find_employee_by_partial_id(get_ID)
            for e in retrieved_employees:
                print(e.emp_id)

        # Checks the Last Name and if entered filters through last names or if entered with employee ID filters by
        # the already filtered ID list
        if get_last_name == '':
            print("No Last Name Entered")
        else:
            if id_entered:
                retrieved_employees = find_employee_by_last_name_filtered(get_last_name, retrieved_employees)
            else:
                retrieved_employees = find_employee_by_last_name_total(get_last_name)

            print("Last Name: " + get_last_name)
            for e in retrieved_employees:
                print(e.last_name)

        y_loc = 0

        # Loops through the retrieved Results and generates a button for each of them which changes the selected ID
        for e in retrieved_employees:
            Button(results_screen, font=("Tahoma", 13, "bold"),
                   text="Last Name: " + e.last_name + "     ID: " + e.emp_id,
                   height=3, width=100, anchor=W, bd=2, bg="#236843",
                   command=(lambda x=e: controller.select_employee(x.emp_id))).place(y=y_loc)
            y_loc += 81

    # Clears the Widgets Each search so they do not overlap one another
    def clear_widgets(self,results_screen):
        for widgets in results_screen.winfo_children():
            widgets.destroy()

if __name__ == "__main__":
    main()
app = Window()
app.mainloop()
