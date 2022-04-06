from tkinter import simpledialog
import system.System_Control as system
from system.Database_Manager import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from pip._internal import main as pipmain

pipmain(['install', 'pillow'])
pipmain(['install', 'tkcalendar'])

from tkcalendar import *
from PIL import ImageTk, Image
from pathlib import Path


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

        self.tk.call('source', Path(__file__).resolve().parent / 'UI' / 'Forest-ttk-theme-master' / 'forest-dark.tcl')

        style.theme_use('forest-dark')

        # Title
        self.title("Employee Management System")

        # Sets the Size of the Window and the Frame
        self.geometry("1000x700")
        container = Frame(self)

        self.iconbitmap(Path(__file__).resolve().parent / 'UI' / 'images' / 'window_icon.ico')

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

    # Shows the user manual pages
    def user_manual(self, page):
        win = Toplevel(self)
        win.geometry("515x515")
        win.title("User Manual")

        img = Image.open(Path(__file__).resolve().parent / 'UI' / 'images' / page)
        user_image = ImageTk.PhotoImage(img)
        win.help_label = Label(win, width=515, height=515, image=user_image)
        win.help_label.image = user_image
        win.help_label.pack()


class Login_Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # Help Button
        img = Image.open(Path(__file__).resolve().parent / 'UI' / 'images' / 'Help.png')
        help_image = ImageTk.PhotoImage(img)
        self.help_button = Button(self, image=help_image, command=lambda: controller.user_manual('Login_Help2.png'))
        self.help_button.image = help_image
        self.help_button.place(x=970, y=2)

        # Creates the Logo Image on the Page
        img = Image.open(Path(__file__).resolve().parent / 'UI' / 'images' / 'Logo.png')
        icon_image = ImageTk.PhotoImage(img)
        self.logo_label = Label(self, width=300, height=175, image=icon_image)
        self.logo_label.image = icon_image
        self.logo_label.place(y=45, x=5)

        # Login Screen Title
        self.title_label = Label(self, text="Employee Management", fg="green", anchor=CENTER,
                                 font=("Tahoma", 18, "underline", "bold"))
        self.title_label.place(height=50, width=300)

        # Login Frame
        self.login_screen = Frame(self, height=600, width=690, bg="gray")
        self.login_screen.place(x=300, y=35)

        # Login labels and entry fields        
        self.login_label = Label(self, text="Please Log In", font=("Tahma", 18))
        self.login_label.place(x=150, y=270, anchor=CENTER)
        self.msg = StringVar()
        self.msg_label = Label(self, textvariable=self.msg, font=("Tahma", 15))
        self.msg_label.place(x=150, y=300, anchor=CENTER)
        self.id_label = Label(self.login_screen, text="Employee ID", bg="grey", font=("Tahoma", 13))
        self.id = StringVar()
        self.id_box = Entry(self.login_screen, textvariable=self.id, bd=1, width=30, font=("Tahoma", 13))
        self.id_label.place(x=180, y=225)
        self.id_box.place(x=280, y=225)
        self.pw = StringVar()
        self.pw_label = Label(self.login_screen, text="Password", bg="grey", font=("Tahoma", 13))
        self.pw_box = Entry(self.login_screen, textvariable=self.pw, bd=1, width=30, show="*", font=("Tahoma", 13))
        self.pw_label.place(x=180, y=275)
        self.pw_box.place(x=280, y=275)

        # Submit button
        self.submit_button = Button(self.login_screen, text="Login", command=lambda: self.retrieve_login(controller),
                                    width=14, bg="grey", font=("Tahoma", 10, "bold"))
        self.submit_button.place(x=345, y=350)

    def retrieve_login(self, controller):
        id_value = self.id.get()
        pw_value = self.pw.get()

        # Add way to save UserName  with chosen_user
        self.msg.set("Invalid Employee ID!")
        for x in total_employees:
            if x.emp_id == id_value:
                if get_password(id_value) == pw_value:
                    self.msg.set("Success!")
                    self.login_success(controller, id_value)
                else:
                    self.msg.set("Invalid password!")

    def login_success(self, controller, id):
        controller.user_id = self.id_box.get()
        controller.select_employee(controller.user_id)


class Employee_Profile_Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Help Button
        img = Image.open(Path(__file__).resolve().parent / 'UI' / 'images' / 'Help.png')
        help_image = ImageTk.PhotoImage(img)
        self.help_button = Button(self, image=help_image, command=lambda: controller.user_manual(
            'Employee_Profile_Help.png'))
        self.help_button.image = help_image
        self.help_button.place(x=970, y=2)

        # Creates the Logo Image on the Page
        img = Image.open(Path(__file__).resolve().parent / 'UI' / 'images' / 'Logo.png')
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
        self.profile_screen.place(x=300, y=35)

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
        self.first_name_entry = Entry(self.profile_screen, bd=1, width=60, textvariable=self.first_name,
                                      font=("Tahoma", 13))
        self.first_name_label.place(x=10, y=50)
        self.first_name_entry.place(x=120, y=50)
        self.last_name = StringVar()
        self.last_name_label = Label(self.profile_screen, text="Last Name:", bg="grey", font=("Tahoma", 13))
        self.last_name_entry = Entry(self.profile_screen, bd=1, width=60, textvariable=self.last_name,
                                     font=("Tahoma", 13))
        self.last_name_label.place(x=10, y=90)
        self.last_name_entry.place(x=120, y=90)
        self.address = StringVar()
        self.address_label = Label(self.profile_screen, text="Address:", bg="grey", font=("Tahoma", 13))
        self.address_entry = Entry(self.profile_screen, bd=1, width=60, textvariable=self.address, font=("Tahoma", 13))
        self.address_label.place(x=10, y=130)
        self.address_entry.place(x=120, y=130)
        self.city = StringVar()
        self.city_label = Label(self.profile_screen, text="City:", bg="grey", font=("Tahoma", 13))
        self.city_entry = Entry(self.profile_screen, bd=1, width=60, textvariable=self.city, font=("Tahoma", 13))
        self.city_label.place(x=10, y=170)
        self.city_entry.place(x=120, y=170)
        self.states_opts = ['AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
                            'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
                            'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
                            'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
                            'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
        self.state = StringVar()
        self.state_label = Label(self.profile_screen, text="State:", bg="grey", font=("Tahoma", 13))
        self.state_drop = OptionMenu(self.profile_screen, self.state, *self.states_opts)
        self.state_label.place(x=10, y=210)
        self.state_drop.place(x=120, y=210)
        self.zip = StringVar()
        self.zip_label = Label(self.profile_screen, text="Zipcode:", bg="grey", font=("Tahoma", 13))
        self.zip_entry = Entry(self.profile_screen, bd=1, width=60, textvariable=self.zip, font=("Tahoma", 13))
        self.zip_label.place(x=10, y=250)
        self.zip_entry.place(x=120, y=250)
        self.phone = StringVar()
        self.phone_label = Label(self.profile_screen, text="Phone:", bg="grey", font=("Tahoma", 13))
        self.phone_entry = Entry(self.profile_screen, bd=1, width=60, textvariable=self.phone, font=("Tahoma", 13))
        self.phone_label.place(x=10, y=290)
        self.phone_entry.place(x=120, y=290)
        self.dob = StringVar()
        self.dob_label = Label(self.profile_screen, text="DOB:", bg="grey", font=("Tahoma", 13))
        self.dob_entry = DateEntry(self.profile_screen, background="white", foreground="black", textvariable=self.dob,
                                   font=("Tahoma", 13))
        self.dob_label.place(x=10, y=330)
        self.dob_entry.place(x=120, y=330)
        self.dept = StringVar()
        self.dept_label = Label(self.profile_screen, text="Department:", bg="grey", font=("Tahoma", 13))
        self.dept_entry = Entry(self.profile_screen, bd=1, width=60, textvariable=self.dept, font=("Tahoma", 13))
        self.dept_label.place(x=10, y=370)
        self.dept_entry.place(x=120, y=370)
        self.title = StringVar()
        self.title_label = Label(self.profile_screen, text="Title:", bg="grey", font=("Tahoma", 13))
        self.title_entry = Entry(self.profile_screen, bd=1, width=60, textvariable=self.title, font=("Tahoma", 13))
        self.title_label.place(x=10, y=410)
        self.title_entry.place(x=120, y=410)
        self.start_date = StringVar()
        self.start_date_label = Label(self.profile_screen, text="Start Date:", bg="grey", font=("Tahoma", 13))
        self.start_date_entry = DateEntry(self.profile_screen, background="white", foreground="black",
                                          textvariable=self.start_date, font=("Tahoma", 13))
        self.start_date_label.place(x=10, y=450)
        self.start_date_entry.place(x=120, y=450)
        self.end_date = StringVar()
        self.end_date_label = Label(self.profile_screen, text="End Date:", bg="grey", font=("Tahoma", 13))
        self.end_date_entry = DateEntry(self.profile_screen, state='disabled', background="white", foreground="black",
                                        textvariable=self.end_date, font=("Tahoma", 13))
        self.end_date_label.place(x=10, y=490)
        self.end_date_entry.place(x=120, y=490)
        self.archived = BooleanVar()
        self.archived_checkbox = Checkbutton(self.profile_screen, text="Archived", bg='grey', selectcolor='black',
                                             variable=self.archived, command=lambda: self.archive_toggle(),
                                             font=("Tahoma", 13))
        self.archived_checkbox.place(x=10, y=530)
        self.is_admin = BooleanVar()
        self.admin_checkbox = Checkbutton(self.profile_screen, text="Admin", bg='grey', selectcolor='black',
                                          variable=self.is_admin, font=("Tahoma", 13))
        self.admin_checkbox.place(x=100, y=530)

        # Save Button
        self.save_button = Button(self, text="Save", width=7, bg="grey", font=("Tahoma", 10, "bold"),
                                  command=lambda: self.save(controller)
                                  )
        self.save_button.place(x=150, y=380, anchor=CENTER)

        # Password Diaplog Button
        self.password_button = Button(self, text="Change Password", width=14, bg="grey", font=("Tahoma", 10, "bold"),
                                      command=lambda: self.new_password_dialog(controller))
        self.password_button.place(x=150, y=420, anchor=CENTER)

        # Payroll Screen Button
        self.payroll_button = Button(self, text="Employee payroll", width=14, bg="grey", font=("Tahoma", 10, "bold"),
                                     command=lambda: controller.show_frame(Employee_Payroll_Screen,
                                                                           controller.chosen_employee))
        self.payroll_button.place(x=150, y=460, anchor=CENTER)

        # Search Screen Button
        self.search_button = Button(self, text="Search Screen", width=14, bg="grey", font=("Tahoma", 10, "bold"),
                                    command=lambda: controller.show_frame(Search_Screen))
        self.search_button.place(x=150, y=500, anchor=CENTER)

    def initiate(self, controller, id):
        '''For the Employee_Profile_Screen this method will check the permissions of the logged in user to determine what they are allowed to edit
        and populates the entry box with data from the given id's employee object'''

        # widget lists
        user_access = [self.address_entry, self.city_entry, self.zip_entry, self.phone_entry]
        admin_access = [self.first_name_entry, self.last_name_entry, self.dept_entry, self.title_entry]
        str_vars = [self.address, self.state, self.city, self.zip, self.phone, self.first_name, self.last_name,
                    self.dob, self.dept, self.title, self.start_date, self.end_date]

        # If id is 0 then starts a new employee with a randomly generated ID.
        if id == '0':
            new_id = str(system.four_random()) + str(system.two_random())
            while find_employee_by_id(new_id) != None:
                new_id = system.four_random() + system.two_random()
            self.emp_id.set(new_id)
            self.arch.set("Enter New Employee")
            self.employee = None
            self.payroll_button.config(state='disabled')
            for i in str_vars:
                i.set('')
            self.archived.set(False)
            self.is_admin.set(False)
            return

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
        if self.archived.get() == True:
            self.arch.set("Employee is INACTIVE")
        else:
            self.arch.set("Employee is ACTIVE")

            # Run permissions check
        # Always sets all Entry to disable first to avoid fields remaining open when switching viewed profiles.
        for i in user_access:
            i.config(state='disabled', disabledbackground="grey", disabledforeground='white')
        for i in admin_access:
            i.config(state='disabled', disabledbackground="grey", disabledforeground='white')
        self.payroll_button.config(state='disabled')
        self.state_drop.config(state='disabled')
        self.archived_checkbox.config(state='disabled')
        self.admin_checkbox.config(state='disabled')
        self.dob_entry.config(state='disabled')
        self.start_date_entry.config(state='disabled')
        self.end_date_entry.config(state='disabled')
        self.mode.set("Read-only Mode")
        # Owned account access
        if controller.user_id == id or controller.admin.get():
            for i in user_access:
                i.config(state='normal')
            self.payroll_button.config(state='normal')
            self.state_drop.config(state='normal')
            self.mode.set("User-Edit Mode")
        # Admin access
        if controller.admin.get():
            for i in admin_access:
                i.config(state='normal')
            self.archive_toggle()
            self.dob_entry.config(state='normal')
            self.start_date_entry.config(state='normal')
            self.archived_checkbox.config(state='normal')
            self.admin_checkbox.config(state='normal')
            self.mode.set("Admin Mode")
        self.first_time_check(controller)

    def archive_toggle(self):
        '''Simple toggle to keep the End date field empty if not archived.'''
        if self.archived.get() == True:
            self.end_date_entry.config(state='normal')
        else:
            self.end_date_entry.config(state='disabled')
            self.end_date.set("None")

    def field_check(self):
        '''Checks fields for invalid entires'''
        field_pass = True
        error_message = ""
        while field_pass == True:
            if self.first_name.get().replace(' ', '').isalpha() == False or self.first_name.get() == "":
                error_message = "Invalid value for First Name. Letter characters only."
                field_pass = False
            if self.last_name.get().replace(' ', '').isalpha() == False or self.last_name.get() == "":
                error_message = "Invalid value for Last Name. Letter characters only."
                field_pass = False
            if self.address.get() == "":
                error_message = "Please enter an address."
                field_pass = False
            if self.city.get().replace(' ', '').isalpha() == False or self.city.get() == "":
                error_message = "Invalid value for City. Letter characters only."
                field_pass = False
            if self.zip.get().replace('-', '').isnumeric() == False or len(self.zip.get().replace('-', '')) < 5:
                error_message = "Invalid value for Zipcode. At least 5 numerical characters only."
                field_pass = False
            if self.phone.get().replace('-', '').replace('Ex:', '').isnumeric() == False or len(
                    self.phone.get().replace('-', '')) < 10:
                error_message = "Invalid value for Phone Number. Include area code, prefix extensions with 'Ex:', numerical characters only."
                field_pass = False
            if self.dept.get().replace(' ', '').isalpha() == False or self.dept.get() == "":
                error_message = "Invalid value for Department. Letter characters only."
                field_pass = False
            if self.title.get().replace(' ', '').isalpha() == False or self.title.get() == "":
                error_message = "Invalid value for Title. Letter characters only."
                field_pass = False
            if self.dob.get() == "":
                error_message = "Please enter a start date."
                field_pass = False
            if self.start_date.get() == "":
                error_message = "Please enter a start date."
                field_pass = False
            if self.archived == True and self.end_date.get() == "None":
                error_message = "Employee is archived, please enter their end date."
                field_pass = False
            break
        if field_pass == False:
            messagebox.showinfo("Message", error_message)
            return False
        else:
            return True

    def save(self, controller):
        '''Saves all entered data to the employee object'''
        # testing check to bipass dialog
        if testing == 1:
            query = 'yes'
        else:
            query = messagebox.askquestion('save', 'save changes?')
        if query == 'yes':
            if self.field_check() == False:
                '''Does not save if field check fails'''
                return
            if self.employee != None:
                self.employee.first_name = self.first_name.get()
                self.employee.last_name = self.last_name.get()
                self.employee.address = self.address.get()
                self.employee.city = self.city.get()
                self.employee.state = self.state.get()
                self.employee.zipcode = self.zip.get()
                self.employee.phone = self.phone.get()
                self.employee.DOB = self.dob_entry.get_date().strftime("%m/%d/%Y")
                self.employee.dept = self.dept.get()
                self.employee.title = self.title.get()
                self.employee.start_date = self.start_date_entry.get_date().strftime("%m/%d/%Y")
                if self.archived.get() == True:
                    self.employee.end_date = self.end_date_entry.get_date().strftime("%m/%d/%Y")
                else:
                    self.employee.end_date = "None"
                self.employee.archive_employee(self.archived.get())
                self.employee.set_admin(self.is_admin.get())
                # Prevents dialog or writing to file in testing
                if testing != 1:
                    messagebox.showinfo("Message", "Save Successful!")
                    system.update_employee_file(total_employees)
            else:
                '''creates new entry for new employee'''
                new_list = [self.emp_id.get(), self.first_name.get(), self.last_name.get(), self.address.get(),
                            self.city.get(), self.state.get(), self.zip.get(), self.phone.get(),
                            self.dob.get(), self.dept.get(), self.title.get(), self.start_date.get(),
                            self.end_date.get(), self.archived.get(), self.is_admin.get()]
                messagebox.showinfo("Message", "Please continue on payroll screen")
                controller.show_frame(Employee_Payroll_Screen, new_list)
        else:
            pass

    def new_password_dialog(self, controller):
        '''Upon User selecting new password, this method will raise a simple dialog box for them to enter the new password'''
        query = simpledialog.askstring("New Password", "Enter New Password.", show="*")
        if query != None:
            set_password(controller.chosen_employee, query)
            messagebox.showinfo("Message", "Password updated!")
        else:
            messagebox.showinfo("Message", "Password not changed!")

    def first_time_check(self, controller):
        '''This method checks if the employee password is at its default for first time users, so it will bring up the new password prompt'''
        # Quick flag to disable this for testing sanity
        if testing == 1:
            return
        default = f"{self.employee.last_name}{self.employee.first_name}{self.employee.SSN[-4:]}"
        if self.employee.get_password() == default and controller.user_id == self.employee.emp_id:
            messagebox.showinfo("Message", "Your password is set to default and needs to change!")
            self.new_password_dialog(controller)


class Reports_Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Help Button
        img = Image.open(Path(__file__).resolve().parent / 'UI' / 'images' / 'Help.png')
        help_image = ImageTk.PhotoImage(img)
        self.help_button = Button(self, image=help_image, command=lambda: controller.user_manual(
            'Paylog_Report_Help.png'))
        self.help_button.image = help_image
        self.help_button.place(x=970, y=2)

        # Title and Return Button
        self.title_label = Label(self, text="Paylog Report", fg="green", font=("Tahoma", 20, "underline"))
        self.emp_profile_button = Button(self, text="Return to Search Screen",
                                         command=lambda: controller.show_frame(Search_Screen))
        self.title_label.pack()
        self.emp_profile_button.place(x=10, y=650)

        f = open(Path(__file__).resolve().parent / 'HoursReports' / 'paylog.txt', "r")
        yloc = 50
        xloc = 0
        for x in f:
            Label(self, text=x, fg="green", font=("Tahoma", 8)).place(x=xloc, y=yloc)
            yloc += 25
            if yloc >= 625:
                xloc += 500
                yloc = 50


class Employee_Payroll_Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # Help Button
        img = Image.open(Path(__file__).resolve().parent / 'UI' / 'images' / 'Help.png')
        help_image = ImageTk.PhotoImage(img)
        self.help_button = Button(self, image=help_image, command=lambda: controller.user_manual(
            'Employee_Payroll_Help.png'))
        self.help_button.image = help_image
        self.help_button.place(x=970, y=2)

        # Creates the Logo Image on the Page
        img = Image.open(Path(__file__).resolve().parent / 'UI' / 'images' / 'Logo.png')
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
        self.profile_screen.place(x=300, y=35)

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
        self.ssn_entry = Entry(self.profile_screen, bd=1, width=55, textvariable=self.ssn, font=("Tahoma", 13))
        self.ssn_label.place(x=10, y=170)
        self.ssn_entry.place(x=150, y=170)
        self.classy_opts = ['Salaried', 'Commissioned', 'Hourly']
        self.classy = StringVar()
        self.classy_label = Label(self.profile_screen, text="classification:", bg="grey", font=("Tahoma", 13))
        self.classy_drop = OptionMenu(self.profile_screen, self.classy, *self.classy_opts)
        self.classy_drop.config(bg="grey", font=("Tahoma", 13))
        self.classy_label.place(x=10, y=210)
        self.classy_drop.place(x=150, y=210)
        self.salary = StringVar()
        self.salary_label = Label(self.profile_screen, text="Salary:", bg="grey", font=("Tahoma", 13))
        self.salary_entry = Entry(self.profile_screen, bd=1, width=55, textvariable=self.salary, font=("Tahoma", 13))
        self.salary_label.place(x=10, y=250)
        self.salary_entry.place(x=150, y=250)
        self.rate = StringVar()
        self.rate_label = Label(self.profile_screen, text="Rate:", bg="grey", font=("Tahoma", 13))
        self.rate_entry = Entry(self.profile_screen, bd=1, width=55, textvariable=self.rate, font=("Tahoma", 13))
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
        self.routing_entry = Entry(self.profile_screen, bd=1, width=55, textvariable=self.routing, font=("Tahoma", 13))
        self.routing_label.place(x=10, y=370)
        self.routing_entry.place(x=150, y=370)
        self.account = StringVar()
        self.account_label = Label(self.profile_screen, text="Account Number:", bg="grey", font=("Tahoma", 13))
        self.account_entry = Entry(self.profile_screen, bd=1, width=55, textvariable=self.account, font=("Tahoma", 13))
        self.account_label.place(x=10, y=410)
        self.account_entry.place(x=150, y=410)

        # Receipt Button
        self.receipt_button = Button(self.profile_screen, text="Add Receipt", width=14, bg="grey",
                                     font=("Tahoma", 10, "bold"),
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
                                     command=lambda: controller.show_frame(Employee_Profile_Screen,
                                                                           controller.chosen_employee))
        self.profile_button.place(x=150, y=420, anchor=CENTER)

        # Search Screen Button
        self.search_button = Button(self, text="Search Screen", width=14, bg="grey", font=("Tahoma", 10, "bold"),
                                    command=lambda: controller.show_frame(Search_Screen))
        self.search_button.place(x=150, y=460, anchor=CENTER)

    def initiate(self, controller, arg):
        '''For the Employee_Payroll_Screen this method will check the permissions of the logged in user to determine what they are allowed to edit
        and populates the entry box with data from the given id's employee object'''

        # widget lists
        user_access = [self.routing_entry, self.account_entry]
        admin_access = [self.salary_entry, self.rate_entry, self.ssn_entry]
        str_vars = [self.routing, self.account, self.salary, self.rate_entry, self.ssn]

        # If there is a list, it is a new employee, leaves entries blank and open
        if isinstance(arg, list):
            self.arch.set("Enter New Employee")
            self.new_list = arg
            self.receipt_button.config(state='disable')
            for i in str_vars:
                i.set('')
            return

        # Run permissions check
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
            self.rate.set(self.employee.pay_rates[2])
            self.receipt_button.config(state='normal')
        elif int(self.employee.classification) == 3:
            self.rate.set(self.employee.pay_rates[1])
            self.salary_entry.config(state='disabled', disabledbackground='grey', disabledforeground='white')
        self.routing.set(self.employee.route)
        self.account.set(self.employee.accounting)
        self.emp_id.set(self.employee.emp_id)
        self.ssn.set(self.employee.SSN)
        if self.employee.archived == 1:
            self.arch.set("Employee is INACTIVE")
        else:
            self.arch.set("Employee is ACTIVE")

    def field_check(self):
        '''Checks fields for invalid entires'''
        field_pass = True
        error_message = ""
        while field_pass == True:
            if self.classy.get() == 'Salaried':
                if self.salary.get().replace('.', '').isnumeric() == False or self.salary.get() == "":
                    error_message = "Invalid value for Salary. Remove commas, numerical characters only."
                    field_pass = False
            if self.classy.get() == 'Commissioned':
                if self.salary.get().replace('.', '').isnumeric() == False or self.salary.get() == "":
                    error_message = "Invalid value for Salary. Remove commas, numerical characters only."
                    field_pass = False
                if self.rate.get().replace('.', '').isnumeric() == False or self.rate.get() == "":
                    error_message = "Invalid value for Rate. Remove commas, numerical characters only."
                    field_pass = False
            if self.classy.get() == 'Hourly':
                if self.rate.get().replace('.', '').isnumeric() == False or self.rate.get() == "":
                    error_message = "Invalid value for Rate. Remove commas, numerical characters only."
                    field_pass = False
            if self.routing.get().replace('-', '')[:-1].isnumeric() == False or 6 > len(
                    self.routing.get().replace('-', '')) > 9:
                error_message = "Invalid value for Routing Number. 6 to 9 digits, numerical characters only with exception of last digit."
                field_pass = False
            if self.account.get().replace('-', '').isnumeric() == False or len(self.account.get().replace('-', '')) < 9:
                error_message = "Invalid value for Routing Number. At least, numerical characters only."
                field_pass = False
            if self.ssn.get().replace('-', '').isnumeric() == False or len(self.ssn.get().replace('-', '')) != 9:
                error_message = "Invalid value for Social Security Number. Must be 9 numerical characters only."
                field_pass = False

            break
        if field_pass == False:
            messagebox.showinfo("Message", error_message)
            return False
        else:
            return True

    def save(self, controller):
        '''Saves all entered data to the employee object ~EXPAND ON THIS LATER, NEEDS CHECKS FOR TRASH ENTRIES!~'''
        # testing check to bipass dialog
        if testing == 1:
            query = 'yes'
        else:
            query = messagebox.askquestion('save', 'save changes?')
        # If there is a list, it is a new Employee, uses the new Employee save
        if query == 'yes':
            if self.field_check() == False:
                '''Does not save if field check fails'''
                return
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
                add = [self.classy.get(), [salary, comm, hourly], self.pay_method.get(), self.routing.get(),
                       self.account.get(), self.ssn.get()]
                self.new_list.extend(add)
                e = Employee(self.new_list[0], self.new_list[2], self.new_list[1], self.new_list[3], self.new_list[4],
                             self.new_list[5], self.new_list[6],
                             self.new_list[15], self.new_list[17], self.new_list[16], self.new_list[18],
                             self.new_list[19], self.new_list[7], self.new_list[20],
                             self.new_list[8], self.new_list[11], self.new_list[12], self.new_list[10],
                             self.new_list[9], self.new_list[13], self.new_list[14])
                total_employees.append(e)
                e.set_default_password()
                controller.select_employee(e.emp_id)
                messagebox.showinfo("Message", "New Employee Added!")
            else:
                if self.classy.get() == 'Salaried':
                    if self.salary.get() != "":
                        self.employee.pay_rates[0] = self.salary.get()
                    self.employee.classification = Salaried(self.employee.pay_rates[0])
                elif self.classy.get() == 'Commissioned':
                    if self.salary.get() != "":
                        self.employee.pay_rates[0] = self.salary.get()
                    if self.rate.get() != "":
                        self.employee.pay_rates[2] = self.rate.get()
                    self.employee.classification = Commissioned(self.employee.pay_rates[0], self.employee.pay_rates[1])
                elif self.classy.get() == 'Hourly':
                    if self.rate.get() != "":
                        self.employee.pay_rates[1] = self.rate.get()
                    self.employee.classification = Hourly(self.employee.pay_rates[2])
                if self.pay_method.get() == 'Direct Deposit':
                    self.employee.payment_method = 2
                else:
                    self.employee.payment_method = 1
                self.employee.route = self.routing.get()
                self.employee.accounting = self.account.get()
                self.employee.SSN = self.ssn.get()
            # Prevents dialog and writing to file in testing
            if testing != 1:
                system.update_employee_file(total_employees)
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

        self.archived = IntVar()
        # Help Button
        img = Image.open(Path(__file__).resolve().parent / 'UI' / 'images' / 'Help.png')
        help_image = ImageTk.PhotoImage(img)
        self.help_button = Button(self, image=help_image, command=lambda: controller.user_manual(
            'Employee_Search_Help.png'))
        self.help_button.image = help_image
        self.help_button.place(x=970, y=2)

        # Creates the Logo Image on the Page
        img = Image.open(Path(__file__).resolve().parent / 'UI' / 'images' / 'Logo.png')
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
        self.results_screen.place(x=300, y=35)

        # Search Button
        self.search_button = Button(self, text="Search", width=7, bg="grey", font=("Tahoma", 10, "bold"),
                                    command=lambda: self.display_results(self.results_screen, controller, self.archived.get())
                                    )
        self.search_button.place(x=125, y=380)

        # Archive Box
        self.archive_box = Checkbutton(self, text="Archived", variable=self.archived, onvalue=1, offvalue=0, selectcolor="green")
        self.archive_box.place(x=200, y=380)
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
    def display_results(self, results_screen, controller, archived):
        print(archived)
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
            retrieved_employees = find_employee_by_partial_id(get_ID,archived)

        # Checks the Last Name and if entered filters through last names or if entered with employee ID filters by
        # the already filtered ID list
        if get_last_name == '':
            print("No Last Name Entered")
        else:
            if id_entered:
                retrieved_employees = find_employee_by_last_name_filtered(get_last_name, retrieved_employees,archived)
            else:
                retrieved_employees = find_employee_by_last_name_total(get_last_name,archived)

            print("Last Name: " + get_last_name)

        y_loc = 0

        # Loops through the retrieved Results and generates a button for each of them which changes the selected ID
        for e in retrieved_employees:
            Button(results_screen, font=("Tahoma", 13, "bold"),
                   text="Last Name: " + e.last_name + "     ID: " + e.emp_id,
                   height=3, width=100, anchor=W, bd=2, bg="#236843",
                   command=(lambda x=e: controller.select_employee(x.emp_id))).place(y=y_loc)
            y_loc += 81

    # Clears the Widgets Each search so they do not overlap one another
    def clear_widgets(self, results_screen):
        for widgets in results_screen.winfo_children():
            widgets.destroy()


def main():
    # Main application launches here
    load_employees()
    if Path(__file__).resolve().parent / 'sytem' / 'employees_updated.csv':
        pass
    else:
        system.update_employee_file(total_employees)
    app = Window()
    app.mainloop()


# uncomment for UI testing and change to 1
testing = 0
# def test():
#     import Login_Test as lt
#     import Profiles_Test as pt
#     import PayScreen_Test as pst
#     load_employees()
#     app = Window()
#     app.after(0, lt.login_series(app.screens[Login_Screen], app))
#     app.after(0, pt.profiles_series(app.screens[Login_Screen], app.screens[Employee_Profile_Screen], app))
#     app.after(0, pst.payscreen_series(app.screens[Login_Screen], app.screens[Employee_Profile_Screen], app.screens[Employee_Payroll_Screen], app))

if __name__ == "__main__":
    main()
# Test stuff, uncomment and comment main to run UI tests
# test()
