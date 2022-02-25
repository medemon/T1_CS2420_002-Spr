from payroll import *
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image

import os, os.path


class Window(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        # Admin Status
        self.admin = True
        # Chosen Employee if viewing information
        self.chosen_employee = ''
        # Styles so the Windows look slightly more appealing
        style = ttk.Style(self)

        self.tk.call('source', os.path.dirname(__file__) + '\\Forest-ttk-theme-master\\forest-dark.tcl')

        style.theme_use('forest-dark')

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
        self.show_frame(Search_Screen)

    # Called when Switching Frames or Screens
    def show_frame(self, cont):
        frame = self.screens[cont]
        frame.tkraise()

    # Checks the Admin status of the current user
    def check_admin(self):
        return self.admin

    # Changes the Variable for the Selected Employee
    def select_employee(self, id):
        self.chosen_employee = id
        print(self.chosen_employee)
        self.show_frame(Employee_Profile_Screen)


class Login_Screen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        print("Logging In")

        self.id_label = Label(self, text="User Name", fg="green", font=("Tahoma", 14))
        self.id_box = Entry(self, width=25, font="Tahoma")

        self.pw_label = Label(self, text="Password", fg="green", font=("Tahoma", 14))
        self.p_box = Entry(self, width=25, font="Tahoma")

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
                    self.login_success(controller)
                else:
                    print("Incorrect Password")

    def login_success(self, controller):
        controller.admin = True
        controller.show_frame(Employee_Profile_Screen)


class Employee_Profile_Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.title_label = Label(self, text="Employee Profile Screen", fg="green", font=("Tahoma", 20))

        self.report_button = Button(self, text="Report Screen",
                                    command=lambda: controller.show_frame(Reports_Screen))

        self.emp_payroll_button = Button(self, text="Employee Payroll",
                                         command=lambda: controller.show_frame(Employee_Payroll_Screen))

        self.admin_screen_button = Button(self, text="Search Screen",
                                          command=lambda: controller.show_frame(Search_Screen))

        # Packs all of the Widgets for the screen
        self.title_label.pack()
        self.report_button.pack()
        self.emp_payroll_button.pack()
        self.admin_screen_button.pack()


class Reports_Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.title_label = Label(self, text="Report Screen", fg="green", font=("Tahoma", 20))

        self.emp_profile_button = Button(self, text="Employee Profile Screen",
                                         command=lambda: controller.show_frame(Employee_Profile_Screen))

        self.title_label.pack()
        self.emp_profile_button.pack()

    pass


class Employee_Payroll_Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.title_label = Label(self, text="Employee Payroll Screen", fg="green", font=("Tahoma", 20))

        self.emp_profile_button = Button(self, text="Employee Profile Screen",
                                         command=lambda: controller.show_frame(Employee_Profile_Screen))

        self.title_label.pack()
        self.emp_profile_button.pack()

    pass


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
        self.new_employee_button.place(x=15, y=450)
        # Report Button

        self.report_button = Button(self, text="Reports Screen",
                                    command=lambda: controller.show_frame(Reports_Screen))
        # Runs an Admin Check
        if controller.check_admin():
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
