from payroll import *
from tkinter import *
from tkinter import ttk


class Window(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # Styles so the Windows look slightly more appealing
        style = ttk.Style(self)

        self.tk.call('source', 'Forest-ttk-theme-master/forest-dark.tcl')

        style.theme_use('forest-dark')

        # Sets the Size of the Window and the Frame
        self.geometry("300x175")
        container = Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Starts up the List of Screens
        self.screens = {}
        # This is the list of classes that it runs through, generates a frame for, then Appends into the Screens list
        for F in (Login_Screen, Employee_Profile_Screen, Reports_Screen, Admin_Screen, Employee_Payroll_Screen):
            frame = F(container, self)

            self.screens[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        # Defaults Screen
        self.show_frame(Login_Screen)

    # Called when Switching Frames or Screens
    def show_frame(self, cont):
        frame = self.screens[cont]
        frame.tkraise()


class Login_Screen(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        print("Logging In")

        self.id_label = Label(self, text="User Name", fg="green", font=("Tahoma", 14))
        self.id_box = Text(self, height=1, width=25, font="Tahoma")

        self.pw_label = Label(self, text="Password", fg="green", font=("Tahoma", 14))
        self.p_box = Text(self, height=1, width=25, font="Tahoma")

        self.submit_button = Button(self, text="Login", command=lambda: self.retrieve_login(controller))

        # Packs all of the Widgets for the screen
        self.id_label.pack()
        self.id_box.pack()

        self.pw_label.pack()
        self.p_box.pack()

        self.submit_button.pack()

    def retrieve_login(self, controller):
        id_value = self.id_box.get("1.0", "end-1c")
        pw_value = self.p_box.get("1.0", "end-1c")
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
        controller.show_frame(Employee_Profile_Screen)


class Employee_Profile_Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.title_label = Label(self, text="Employee Profile Screen", fg="green", font=("Tahoma", 20))

        self.report_button = Button(self, text="Report Screen",
                                    command=lambda: controller.show_frame(Reports_Screen))

        self.emp_payroll_button = Button(self, text="Employee Payroll",
                                         command=lambda: controller.show_frame(Employee_Payroll_Screen))

        self.admin_screen_button = Button(self, text="Admin Screen",
                                          command=lambda: controller.show_frame(Admin_Screen))

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


class Admin_Screen(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.title_label = Label(self, text="Admin Screen", fg="green", font=("Tahoma", 20))

        self.emp_profile_button = Button(self, text="Employee Profile Screen",
                                         command=lambda: controller.show_frame(Employee_Profile_Screen))

        self.title_label.pack()
        self.emp_profile_button.pack()
    pass


if __name__ == "__main__":
    main()
app = Window()
app.mainloop()
