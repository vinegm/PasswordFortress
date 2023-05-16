import tkinter as tk
from src.utils import *


class RegisterFrame(tk.Frame):
    """Frame responsable for registering a user in the app

    Attributes:
    Connection: Database of the app
    master: Widget/window where this frame will be loaded
    controller: Main class of the app

    Methods:
    _registerUser: Registers a user if all the "if's" are passed and returns to the LoginFrame
    _return: Returns to the LoginFrame and clears all the widgets from this one
    """
    def __init__(self, connection, master, controller):
        tk.Frame.__init__(self, master)
        self.columnconfigure(0, minsize=100)
        self.columnconfigure(1, minsize=200)
        
        # Header Label
        self.header = tk.Label(self,
                     text = "Register an Account!",
                     font = ("Arial", 12, "bold"))
        self.header.grid(pady = 20,
                  padx = 10,
                  row = 0,
                  column = 0, columnspan = 2,
                  sticky="nsew")
        
        # Nickname label and entry
        nicknameLabel = tk.Label(self,
                              text = "Nickname:",
                              font = ("Arial", 9, "bold"))
        nicknameLabel.grid(pady = 5,
                           row = 1,
                           column = 0,
                           sticky = "e")
        
        self.nicknameEntry = tk.Entry(self)
        self.nicknameEntry.grid(pady = 5,
                           row = 1,
                           column = 1,
                           sticky = "w")
        
        # Set focus to next box
        self.nicknameEntry.bind("<Return>", lambda event: self.usernameEntry.focus_set())

        # Username label and entry
        usernameLabel = tk.Label(self,
                              text = "Username:",
                              font = ("Arial", 9, "bold"))
        usernameLabel.grid(pady = 5,
                           row = 2,
                           column = 0,
                           sticky = "e")
        
        self.usernameEntry = tk.Entry(self)
        self.usernameEntry.grid(pady = 5,
                           row = 2,
                           column = 1,
                           sticky = "w")
        self.usernameEntry.bind("<Return>", lambda event: self.passwordEntry.focus_set())

        # Password label and entry
        passwordLabel = tk.Label(self,
                              text = "Password:",
                              font = ("Arial", 9, "bold"))
        passwordLabel.grid(pady = 5,
                           row = 3,
                           column = 0,
                           sticky = "e")
        
        self.passwordEntry = tk.Entry(self, show = "*")  # Password box only shows * insted of the password
        self.passwordEntry.grid(pady = 5,
                           row = 3,
                           column = 1,
                           sticky = "w")
        self.passwordEntry.bind("<Return>", lambda event: self.confirmPasswordEntry.focus_set())

        # Password Confirmation label and entry
        confirmPasswordLabel = tk.Label(self,
                                     text = "Confirm\nPassword:",
                                     font = ("Arial", 9, "bold"))
        confirmPasswordLabel.grid(pady = 5,
                                  row = 4,
                                  column = 0,
                                  sticky = "e")
        
        self.confirmPasswordEntry = tk.Entry(self, show = "*")  # Password confirmation box only shows *
        self.confirmPasswordEntry.grid(pady = 5,
                                  row = 4,
                                  column = 1,
                                  sticky = "w")

        # Button and bind responsable for calling the register function
        self.confirmPasswordEntry.bind("<Return>", lambda event: self._registerUser(controller, connection))
        RegisterButton = tk.Button(self,
                                text = "Register")
        RegisterButton.grid(row = 5,
                            column = 0, columnspan = 2,
                            sticky= "ns")
        RegisterButton.bind("<Button-1>", lambda event: self._registerUser(controller, connection))

        # Goes back to the login screen without registering the user
        backLabel = tk.Label(self,
                          text = "Back",
                          font = ("Arial", 7, "bold", "underline"),
                          fg = "Blue")
        backLabel.bind("<Button-1>", lambda event: self._return(controller))
        backLabel.grid(row = 5,
                       column= 0,
                       sticky = "ew")

    def _registerUser(self, controller, connection):
        """Registers a user if all the "if's" are passed and returns to the LoginFrame

        Parameters:
        controller: Main class of the app
        connection: database of the app
        """
        # If a box is left empty
        if self.nicknameEntry.get() == "" or self.usernameEntry.get() == "" or self.passwordEntry.get() == "":
            self.header.config(text = "Fill All The Boxes!")
            return

        # If a username is already in use
        if user_exists(username := hash_info(self.usernameEntry.get()), connection) != False:
            self.header.config(text = "Username Unavailable!")
            return

        # If password and the password confirmation dont match
        if self.confirmPasswordEntry.get() != self.passwordEntry.get():
            self.header.config(text = "Passwords Don't Match!")
            return

        # Registers the user if everything is ok
        nickname = self.nicknameEntry.get()
        password = hash_info(self.passwordEntry.get())
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (nickname, username, password) VALUES (?, ?, ?)", (nickname, username, password))
        connection.commit()
        cursor.close()
        self._return(controller)

    def _return(self, controller):
        """Returns to the LoginFrame and clears all the widgets from this one
        
        Parameters:
        Controller: Main class of the app, used to call the function to change frame
        """
        for selectEntry in (self.nicknameEntry, self.usernameEntry, self.passwordEntry, self.confirmPasswordEntry):
            selectEntry.delete(0, tk.END)
        self.header.config(text = "Register an Account!")
        controller.change_frame("LoginFrame")
