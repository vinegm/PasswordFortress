"""
Password manager
 The project focus on making a desktop app that stores the users accounts safely in a friendly and simple way
"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from io import BytesIO
import sqlite3
import hashlib


def setDatabase (connection):
    """If the database doesnt exist in the directory, creates it
    
    Parameters:
    connection: SQLite3 connection to a data base
    """
    cursor = connection.cursor()
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
    result = cursor.fetchone()
    if result[0] == 0:
        cursor.execute("""CREATE TABLE users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nickname VARCHAR,
                       username VARCHAR UNIQUE,
                       password VARCHAR)""")
        cursor.execute("""CREATE TABLE accounts
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       plataform VARCHAR,
                       login VARCHAR,
                       password VARCHAR,
                       logo BLOB,
                       user_id INTEGER,
                       FOREIGN KEY (user_id) REFERENCES users(id))""")
        connection.commit()
    
    cursor.close()
    return


def userExists(search, connection):
    """Checks if a user exists on the database
    
    Parameters:
    search: User to be searched for in the database
    connection: Database that will be searched

    Returns:
    False: If the user doesnt exist
    result: A tuple with the user information
    """
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (search,))
    result = cursor.fetchone()
    cursor.close()
    if result == None:
        return False
    return result


def getAccounts(userId, connection):
    """Gets all the accounts of a given user

    Parameters:
    UserId: Id of the user in the database
    connection: Database that will be searched

    returns:
    accounts: All the accounts from the user in a tuple
    """
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM accounts WHERE user_id = ?", (userId,))
    accounts = cursor.fetchall()
    cursor.close()
    return accounts


def hashInfo(info):
    """Takes a paramater and hashed it using the hash function blake2b

    Parameters:
    info (any): Value to be hashed

    Returns:
    The hashed info
    """
    return hashlib.blake2b(info.encode()).hexdigest()


class PasswordManager(tk.Tk):
    """Main class of the app, starts the database and frames

    Methods:
    changeFrame(): Changes between existing frames
    """
    def __init__(self):
        tk.Tk.__init__(self)

        connection = sqlite3.connect("UsersInfo.db")
        setDatabase(connection)

        self.title("Password Manager")
        self.geometry("300x250")
        self.eval("tk::PlaceWindow . center")
        self.iconbitmap("assets/Key.ico")
        
        framesHolder = tk.Frame(self)
        framesHolder.pack(anchor = "center")
        
        self.frames = {}
        for F in (LoginFrame, RegisterFrame):
            page_name = F.__name__
            frame = F(connection, framesHolder, self)
            self.frames[page_name] = frame
            frame.grid(row = 0,
                       column = 0,
                       sticky = "nsew")
    
        self.changeFrame("LoginFrame")

    def changeFrame(self, nextFrame):
        """Changes between existing frames

        Parameters:
        nextFrame: Frame that will be raised 
        """
        frame = self.frames[nextFrame]
        frame.tkraise()
        if nextFrame == "LoginFrame":
            self.resizable(True,True)
            self.geometry("300x175")

        elif nextFrame == "RegisterFrame":
            self.resizable(True,True)
            self.geometry("300x240")

        else:
            self.resizable(True,True)
            self.geometry("700x700")

        self.resizable(False, False)


class LoginFrame(tk.Frame):
    """Frame responsable for login a user in the app

    Attributes:
    Connection: Database of the app
    master: Widget/window where this frame will be loaded
    controller: Main class of the app 

    Methods:
    _loginUser: Checks if username and password match a user and logs said user
    _changeAndClearFrame: Changes the raised frame and clear the widgets in this one
    """
    def __init__(self, connection, master, controller):
        tk.Frame.__init__(self, master)
        self.columnconfigure(0, minsize=100)
        self.columnconfigure(1, minsize=200)
        
        # Header label
        self.header = tk.Label(self,
                     text = "Welcome to a Password Manager!",
                     font = ("Arial", 12, "bold"))
        self.header.grid(pady = 20,
                  padx = 10,
                  row = 0,
                  column = 0, columnspan = 2,
                  sticky="nsew")

        # Username label and entry
        usernameLabel = tk.Label(self,
                              text = "Username:",
                              font = ("Arial", 9, "bold"))
        usernameLabel.grid(pady = 5,
                           row = 1,
                           column = 0,
                           sticky = "e")

        self.usernameEntry = tk.Entry(self)
        self.usernameEntry.grid(pady = 5,
                           row = 1,
                           column = 1,
                           sticky = "w")
        
        # Bind to set focus on the password entry once username is entered
        self.usernameEntry.bind("<Return>", lambda event: self.passwordEntry.focus_set())

        # Password label and entry
        passwordLabel = tk.Label(self,
                              text = "Password:",
                              font = ("Arial", 9, "bold"))
        passwordLabel.grid(pady = 5,
                           row = 2,
                           column = 0,
                           sticky = "e")

        self.passwordEntry = tk.Entry(self, show = "*")
        self.passwordEntry.grid(pady = 5,
                           row = 2,
                           column = 1,
                           sticky = "w")


        # Register label and entry, responsable for sending the user to a register screen if needed
        registerLabel = tk.Label(self,
                              text = "Register",
                              font = ("Arial", 7, "bold", "underline"),
                              fg = "Blue")
        registerLabel.bind("<Button-1>", lambda event: self._changeAndClearFrame("RegisterFrame", controller)) 
        registerLabel.grid(pady = 5,
                           row = 3,
                           column= 0)

        
        # Button and bind responsable for calling the login function
        self.passwordEntry.bind("<Return>", lambda event: self._loginUser(master, controller, connection))
        LoginButton = tk.Button(self,
                                text = "Login")
        LoginButton.grid(pady = 10,
                         row = 3,
                         column = 0, columnspan = 2,
                         sticky= "ns")
        LoginButton.bind("<Button-1>", lambda event: self._loginUser(master, controller, connection))
        
    def _loginUser (self, master, controller, connection):
        """Checks if username and password match a user and logs said user

        Parameters:
        master: Frame that holds the loaded frames
        controller: Window of the app
        connection: Main class of the app
        """
        hashedUser = hashInfo(self.usernameEntry.get())
        userInfo = userExists(hashedUser, connection)
        if userInfo == False:
            self.header.config(text = "Username/Password Incorrect!")
            return
        
        userPassword = userInfo[3]
        if hashInfo(self.passwordEntry.get()) != userPassword:
            self.header.config(text = "Username/Password Incorrect!")
            return
        
        page_name = ProfileFrame.__name__
        frame = ProfileFrame(connection, master, controller, userInfo)
        controller.frames[page_name] = frame
        frame.grid(row = 0,
                column = 0,
                sticky = "nsew")
        self._changeAndClearFrame("ProfileFrame", controller)

    def _changeAndClearFrame(self, nextFrame, controller):
        """Changes the raised frame and clear the widgets in this one

        Parameters:
        nextFrame: frame that will be raised
        """
        for selectEntry in (self.usernameEntry, self.passwordEntry):
            selectEntry.delete(0, tk.END)
        self.header.config(text = "Welcome to a Password Manager!")
        controller.changeFrame(nextFrame)

# Class responsable for the register screen
class RegisterFrame(tk.Frame):
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

    # Registers the user
    def _registerUser(self, controller, connection):
        # If a box is left empty
        if self.nicknameEntry.get() == "" or self.usernameEntry.get() == "" or self.passwordEntry.get() == "":
            self.header.config(text = "Fill All The Boxes!")
            return

        # If a username is already in use
        if userExists(username := hashInfo(self.usernameEntry.get()), connection) != False:
            self.header.config(text = "Username Unavailable!")
            return

        # If password and the password confirmation dont match
        if self.confirmPasswordEntry.get() != self.passwordEntry.get():
            self.header.config(text = "Passwords Don't Match!")
            return

        # Registers the user if everything is ok
        nickname = self.nicknameEntry.get()
        password = hashInfo(self.passwordEntry.get())
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (nickname, username, password) VALUES (?, ?, ?)", (nickname, username, password))
        connection.commit()
        cursor.close()
        self._return(controller)

    # Returns to the login screen and clears all the entrys in the register screen
    def _return(self, controller):
        for selectEntry in (self.nicknameEntry, self.usernameEntry, self.passwordEntry, self.confirmPasswordEntry):
            selectEntry.delete(0, tk.END)
        self.header.config(text = "Register an Account!")
        controller.changeFrame("LoginFrame")

class ProfileFrame(tk.Frame):
    def __init__(self, connection, master, controller, userInfo):
        tk.Frame.__init__(self, master)
        self.userInfo = userInfo
        # Header label
        header = tk.Label(self,
                          text = self.userInfo[1],
                          font = ("Arial", 20, "bold"))
        header.pack(anchor = "center",
                    fill = "x")
        
        # Logoff Label
        logoff = tk.Label(header,
                          text = "Logoff",
                          font = ("Arial", 15, "bold"),
                          fg = "red")
        logoff.pack(anchor = "nw")

        logoff.bind("<Button-1>", lambda evenet: self._logoff(controller))

        # Separator from the Username and accounts
        headerSeparator = tk.Canvas(self,
                                width = 700,
                                height = 5)
        headerSeparator.pack(anchor = "n")
        headerSeparator.create_line(0, 3, 700, 3, width = 3, fill = "black")
                
        # Canvas with scrollbar
        self.canvas = tk.Canvas(self, width = 680, height = 650)
        self.canvas.pack(side="left", fill="both")

        scrollbar = ttk.Scrollbar(self, orient = "vertical", command = self.canvas.yview)
        scrollbar.pack(side="right",fill="y")

        self.canvas.configure(yscrollcommand = scrollbar.set)

        self._loadAccounts(connection)


    def _loadAccounts(self, connection):
        self.accountsHolder = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window = self.accountsHolder, anchor = "nw")
        
        for i in range(4):
            self.accountsHolder.columnconfigure(i, minsize = 175)

        self.accounts = {}
        accounts = getAccounts(self.userInfo[0], connection)
        
        for row, account in enumerate(accounts):
            accountId, plataform, login, password, logo = account[0:5]
            self.listAccount(accountId, plataform, login, password, logo, row, self.accountsHolder, connection)
        
        plusImage = Image.open("assets/Plus_Icon.png")
        plusImage.thumbnail((75, 75))
        plusImage = ImageTk.PhotoImage(plusImage)

        addPlataformButton = tk.Button(self.accountsHolder,
                                        image = plusImage)
        addPlataformButton.bind("<Button-1>", lambda event: self._addAccount(connection))
        addPlataformButton.grid(column = 1, columnspan = 2,
                                sticky = "s")
        addPlataformButton.image = plusImage
        
        self.accountsHolder.update_idletasks()
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))
        
    def _addAccount(self, connection):
        popup = tk.Toplevel()
        popup.title("Add Account")

        widgets = tk.Frame(popup)
        widgets.pack(anchor = "center")

        def _addLogo():
            logoPath = filedialog.askopenfilename()
            logoImg = Image.open(logoPath)
            logoImg.thumbnail((100, 100))
            with open(logoPath, "rb") as file:
                _saveAccount.logoBytes = file.read()

            logoImg = ImageTk.PhotoImage(logoImg)
            addPlataformLogo.config(image = logoImg)
            addPlataformLogo.image = logoImg

        placeHolder = Image.open("assets/Question_Mark.png")
        placeHolder.thumbnail((100, 100))
        placeHolder = ImageTk.PhotoImage(placeHolder)

        addPlataformLogo = tk.Label(widgets, image = placeHolder)
        addPlataformLogo.grid(row = 0, rowspan = 3,
                                column = 0)
        addPlataformLogo.image = placeHolder

        addPlataformLogo.bind("<Button-1>", lambda event: _addLogo())

        addPlataformLabel = tk.Label(widgets, text = "Plataform:")
        addPlataformLabel.grid(row = 0,
                                column = 1)

        addPlataformEntry = tk.Entry(widgets)
        addPlataformEntry.grid(row = 0,
                                column = 2)
        addPlataformEntry.bind("<Return>", lambda event: addLoginEntry.focus_set())

        addLoginLabel = tk.Label(widgets, text = "Login:")
        addLoginLabel.grid(row = 1,
                            column = 1)

        addLoginEntry = tk.Entry(widgets)
        addLoginEntry.grid(row = 1,
                            column = 2)
        addLoginEntry.bind("<Return>", lambda event: addPasswordEntry.focus_set())
        
        addPasswordLabel = tk.Label(widgets, text = "Password:")
        addPasswordLabel.grid(row = 2,
                                column = 1)

        addPasswordEntry = tk.Entry(widgets)
        addPasswordEntry.grid(row = 2,
                                column = 2)
        
        
        def _saveAccount():
            cursor = connection.cursor()
            try:
                account = [addPlataformEntry.get(), addLoginEntry.get(), addPasswordEntry.get(), _saveAccount.logoBytes, self.userInfo[0]]
                cursor.execute("INSERT INTO accounts (plataform, login, password, logo, user_id) VALUES (?, ?, ?, ?, ?)", (account))
            except AttributeError:
                account = [addPlataformEntry.get(), addLoginEntry.get(), addPasswordEntry.get(), self.userInfo[0]]
                cursor.execute("INSERT INTO accounts (plataform, login, password, user_id) VALUES (?, ?, ?, ?)", (account))
            connection.commit()
            cursor.close()
            
            self._reloadAccounts(connection)
            popup.destroy()

        saveButton = tk.Button(widgets,
                                text = "Add",
                                command = _saveAccount)
        saveButton.grid(row = 3,
                        column = 0, columnspan = 3)
    
    def _reloadAccounts(self, connection):
        self.accountsHolder.destroy()
        self._loadAccounts(connection)
    
    def listAccount(self, accountId, plataform, login, password, logo, frameRow, holder, connection):
        accountFrame = tk.Frame(holder)
        accountFrame.grid(row = (frameRow),
                        column = 0, columnspan = 4,
                        sticky = "nsew")
        
        self.accounts[accountId] = accountFrame

        accountFrame.columnconfigure(0, minsize = 110)
        accountFrame.columnconfigure(1, minsize = 370)
        accountFrame.columnconfigure(2, minsize = 110)
        accountFrame.columnconfigure(3, minsize = 110)

        if logo != None:
            logo = Image.open(BytesIO(logo))
            logo.thumbnail((100, 100))
            logo = ImageTk.PhotoImage(logo)
            plataformLogo = tk.Label(accountFrame, image = logo)
            plataformLogo.image = logo
        else:
            placeHolder = Image.open("assets/Question_Mark.png")
            placeHolder.thumbnail((100, 100))
            placeHolder = ImageTk.PhotoImage(placeHolder)
            plataformLogo = tk.Label(accountFrame, image = placeHolder)
            plataformLogo.image = placeHolder

        plataformLogo.grid(row = 0, rowspan = 3,
                        column = 0,
                        sticky = "w")
        plataformLogo.bind("<Button-1>", lambda event: _changeLogo(accountId))

        plataformLabel = tk.Label(accountFrame,
                                text = plataform)
        plataformLabel.grid(row = 0,
                            column = 1,
                            sticky = "w")

        loginLabel = tk.Label(accountFrame,
                            text = login)
        loginLabel.grid(row = 1,
                        column = 1,
                        sticky = "w")

        passwordLabel = tk.Label(accountFrame,
                                text = password)
        passwordLabel.grid(row = 2,
                        column = 1,
                        sticky = "w")

        def _deleteAccount(accountId):
            cursor = connection.cursor()
            cursor.execute("DELETE FROM accounts WHERE id = ?", (accountId,))
            connection.commit()
            cursor.close()
            self._reloadAccounts(connection)

        deleteIcon = Image.open("assets/Delete.png")
        deleteIcon.thumbnail((75, 75))
        deleteIcon = ImageTk.PhotoImage(deleteIcon)

        deleteButton = tk.Button(accountFrame,
                                image = deleteIcon)
        deleteButton.image = deleteIcon
        deleteButton.grid(row = 0, rowspan = 3,
                        column = 3,
                        sticky = "w")
        deleteButton.bind("<Button-1>", lambda evenet: _deleteAccount(accountId))

        def _editAccount(accountId):
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM accounts WHERE id = ?", (accountId,))
            account = cursor.fetchmany()
            cursor.close()
            
            popup = tk.Toplevel()
            popup.title("Edit Account")

            widgets = tk.Frame(popup)
            widgets.pack(anchor = "center")

            editPlataformLabel = tk.Label(widgets, text = "Plataform:")
            editPlataformLabel.grid(row = 0,
                                   column = 1)

            editPlataformEntry = tk.Entry(widgets)
            editPlataformEntry.insert(0, account[0][1])
            editPlataformEntry.grid(row = 0,
                                    column = 2)
            editPlataformEntry.bind("<Return>", lambda event: editLoginEntry.focus_set())

            editLoginLabel = tk.Label(widgets, text = "Login:")
            editLoginLabel.grid(row = 1,
                                column = 1)

            editLoginEntry = tk.Entry(widgets)
            editLoginEntry.insert(0, account[0][2])
            editLoginEntry.grid(row = 1,
                                column = 2)
            editLoginEntry.bind("<Return>", lambda event: editPasswordEntry.focus_set())
            
            editPasswordLabel = tk.Label(widgets, text = "Password:")
            editPasswordLabel.grid(row = 2,
                                   column = 1)

            editPasswordEntry = tk.Entry(widgets)
            editPasswordEntry.insert(0, account[0][3])
            editPasswordEntry.grid(row = 2,
                                   column = 2)

            def _saveEdit():
                cursor = connection.cursor()
                cursor.execute("UPDATE accounts SET plataform = ?, login = ?, password = ? WHERE id = ?", (editPlataformEntry.get(), editLoginEntry.get(), editPasswordEntry.get(), account[0][0],))
                connection.commit()
                cursor.close()
                self._reloadAccounts(connection)
                popup.destroy()

            saveEditButton = tk.Button(widgets,
                                       text = "Save",
                                       command = _saveEdit)
            saveEditButton.grid(row = 3,
                                column = 0, columnspan = 3)

        editIcon = Image.open("assets/Edit.png")
        editIcon.thumbnail((75, 75))
        editIcon = ImageTk.PhotoImage(editIcon)

        editButton = tk.Button(accountFrame,
                            image = editIcon)
        editButton.image = editIcon
        editButton.grid(row = 0, rowspan = 3,
                        column = 2,
                        sticky = "w")
        editButton.bind("<Button-1>", lambda evenet: _editAccount(accountId))
        
        separator = tk.Canvas(accountFrame,
                            width = 700,
                            height = 5)
        separator.grid(row = 3,
                    column = 0, columnspan = 4,
                    sticky = "s")
        separator.create_line(0, 3, 700, 3, width = 3, fill = "black")

        def _changeLogo(accountId):
            logoPath = filedialog.askopenfilename()
            logoImg = Image.open(logoPath)
            logoImg.thumbnail((100, 100))
            with open(logoPath, "rb") as file:
                logoBytes = file.read()
            
            cursor = connection.cursor()
            cursor.execute("UPDATE accounts SET logo = ? WHERE id = ?", (logoBytes, accountId,))
            connection.commit()
            cursor.close()

            logoImg = ImageTk.PhotoImage(logoImg)
            accountFrame = self.accounts[accountId]
            plataformLogo = accountFrame.children["!label"]
            plataformLogo.config(image = logoImg)
            plataformLogo.image = logoImg

    def _logoff(self, controller):
            self.destroy()
            controller.changeFrame("LoginFrame")



if __name__ == '__main__':
    window = PasswordManager()    
    window.mainloop()