import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from io import BytesIO
import sqlite3
import hashlib

# Checks if user exists in the database, if not, returns false, if the user exists returns the hashed password
def userExists(search):
    cursor.execute("SELECT * FROM users WHERE username = ?", (search,))
    result = cursor.fetchone()
    if result == None:
        return False
    return result


def getAccounts(userId):
    cursor.execute("SELECT * FROM accounts WHERE user_id = ?", (userId,))
    accounts = cursor.fetchall()
    return accounts


# Hashed the info given to it, used to simplify code
def hashInfo(info):
    return hashlib.md5(info.encode()).hexdigest()


def listAccount(accountId, plataform, login, password, logo, frameRow, holder, master):
    accountFrame = tk.Frame(holder)
    accountFrame.grid(row = (frameRow),
                      column = 0, columnspan = 4,
                      sticky = "nsew")
    
    master.accounts[accountId] = accountFrame

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
        cursor.execute("DELETE FROM accounts WHERE id = ?", (accountId,))
        connection.commit()
        master._reloadAccounts()

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
        print(accountId)
        master._reloadAccounts()

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
            
        cursor.execute("UPDATE accounts SET logo = ? WHERE id = ?", (logoBytes, accountId,))
        connection.commit()

        logoImg = ImageTk.PhotoImage(logoImg)
        accountFrame = master.accounts[accountId]
        plataformLogo = accountFrame.children["!label"]
        plataformLogo.config(image = logoImg)
        plataformLogo.image = logoImg


# Class responsable to loading the frames and app
class PasswordManager(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("Password Manager")
        self.geometry("300x250")
        self.eval("tk::PlaceWindow . center")
        self.iconbitmap("assets/Key.ico")
        
        framesHolder = tk.Frame(self)
        framesHolder.pack(anchor = "center")
        
        self.frames = {}
        for F in (LoginFrame, RegisterFrame): #, ProfileFrame):
            page_name = F.__name__
            frame = F(framesHolder, self)
            self.frames[page_name] = frame
            frame.grid(row = 0,
                       column = 0,
                       sticky = "nsew")
    
        self.changeFrame("LoginFrame")

    # Function responsable for changing the frames, loading one on top of another
    def changeFrame(self, nextFrame):
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



# Class responsable for the login screen
class LoginFrame(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.columnconfigure(0, minsize=100)
        self.columnconfigure(1, minsize=200)
        
        # Header label
        header = tk.Label(self,
                     text = "Welcome to a Password Manager!",
                     font = ("Arial", 12, "bold"))
        header.grid(pady = 20,
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

        usernameEntry = tk.Entry(self)
        usernameEntry.grid(pady = 5,
                           row = 1,
                           column = 1,
                           sticky = "w")
        
        # Bind to set focus on the password entry once username is entered
        usernameEntry.bind("<Return>", lambda event: passwordEntry.focus_set())

        # Password label and entry
        passwordLabel = tk.Label(self,
                              text = "Password:",
                              font = ("Arial", 9, "bold"))
        passwordLabel.grid(pady = 5,
                           row = 2,
                           column = 0,
                           sticky = "e")

        passwordEntry = tk.Entry(self, show = "*")
        passwordEntry.grid(pady = 5,
                           row = 2,
                           column = 1,
                           sticky = "w")

        def _changeAndClearFrame(nextFrame):
            for selectEntry in (usernameEntry, passwordEntry):
                selectEntry.delete(0, tk.END)
            header.config(text = "Welcome to a Password Manager!")
            controller.changeFrame(nextFrame)

        # Register label and entry, responsable for sending the user to a register screen if needed
        RegisterLabel = tk.Label(self,
                              text = "Register",
                              font = ("Arial", 7, "bold", "underline"),
                              fg = "Blue")
        RegisterLabel.bind("<Button-1>", lambda event: _changeAndClearFrame("RegisterFrame")) 
        RegisterLabel.grid(pady = 5,
                           row = 3,
                           column= 0)

        # Function responsable for checking if the user and password are registered in the system and login
        def _loginUser (*event):
            if (userInfo := userExists(hashInfo(usernameEntry.get()))) == False:
                header.config(text = "Username/Password Incorrect!")

            elif hashInfo(passwordEntry.get()) != userInfo[3]:
                header.config(text = "Username/Password Incorrect!")
                
            else:
                page_name = ProfileFrame.__name__
                frame = ProfileFrame(master, controller, userInfo)
                controller.frames[page_name] = frame
                frame.grid(row = 0,
                        column = 0,
                        sticky = "nsew")
                _changeAndClearFrame("ProfileFrame")
        
        # Button and bind responsable for calling the login function
        passwordEntry.bind("<Return>", _loginUser)
        LoginButton = tk.Button(self,
                                text = "Login",
                                command = _loginUser)
        LoginButton.grid(pady = 10,
                         row = 3,
                         column = 0, columnspan = 2,
                         sticky= "ns")


# Class responsable for the register screen
class RegisterFrame(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master)
        self.columnconfigure(0, minsize=100)
        self.columnconfigure(1, minsize=200)
        
        # Header Label
        head = tk.Label(self,
                     text = "Register an Account!",
                     font = ("Arial", 12, "bold"))
        head.grid(pady = 20,
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
        
        nicknameEntry = tk.Entry(self)
        nicknameEntry.grid(pady = 5,
                           row = 1,
                           column = 1,
                           sticky = "w")
        
        # Set focus to next box
        nicknameEntry.bind("<Return>", lambda event: usernameEntry.focus_set())

        # Username label and entry
        usernameLabel = tk.Label(self,
                              text = "Username:",
                              font = ("Arial", 9, "bold"))
        usernameLabel.grid(pady = 5,
                           row = 2,
                           column = 0,
                           sticky = "e")
        
        usernameEntry = tk.Entry(self)
        usernameEntry.grid(pady = 5,
                           row = 2,
                           column = 1,
                           sticky = "w")
        usernameEntry.bind("<Return>", lambda event: passwordEntry.focus_set())

        # Password label and entry
        passwordLabel = tk.Label(self,
                              text = "Password:",
                              font = ("Arial", 9, "bold"))
        passwordLabel.grid(pady = 5,
                           row = 3,
                           column = 0,
                           sticky = "e")
        
        passwordEntry = tk.Entry(self, show = "*")  # Password box only shows * insted of the password
        passwordEntry.grid(pady = 5,
                           row = 3,
                           column = 1,
                           sticky = "w")
        passwordEntry.bind("<Return>", lambda event: confirmPasswordEntry.focus_set())

        # Password Confirmation label and entry
        confirmPasswordLabel = tk.Label(self,
                                     text = "Confirm\nPassword:",
                                     font = ("Arial", 9, "bold"))
        confirmPasswordLabel.grid(pady = 5,
                                  row = 4,
                                  column = 0,
                                  sticky = "e")
        
        confirmPasswordEntry = tk.Entry(self, show = "*")  # Password confirmation box only shows *
        confirmPasswordEntry.grid(pady = 5,
                                  row = 4,
                                  column = 1,
                                  sticky = "w")

        # Returns to the login screen and clears all the entrys in the register screen
        def _return(*event):
            controller.changeFrame("LoginFrame")
            for selectEntry in (nicknameEntry, usernameEntry, passwordEntry, confirmPasswordEntry):
                selectEntry.delete(0, tk.END)
            head.config(text = "Register an Account!")

        # Registers the user
        def _registerUser(*event):
            # If a box is left empty
            if nicknameEntry.get() == "" or usernameEntry.get() == "" or passwordEntry.get() == "":
                head.config(text = "Fill All The Boxes!")

            # If a username is already in use
            elif userExists(username := hashInfo(usernameEntry.get())) != False:
                head.config(text = "Username Unavailable!")

            # If password and the password confirmation dont match
            elif confirmPasswordEntry.get() != passwordEntry.get():
                head.config(text = "Passwords Don't Match!")

            # Registers the user if everything is ok
            else:
                nickname = nicknameEntry.get()
                password = hashInfo(passwordEntry.get())
                cursor.execute("INSERT INTO users (nickname, username, password) VALUES (?, ?, ?)", (nickname, username, password))
                connection.commit()
                _return()

        # Button and bind responsable for calling the register function
        confirmPasswordEntry.bind("<Return>", _registerUser)
        RegisterButton = tk.Button(self,
                                text = "Register",
                                command = _registerUser)
        RegisterButton.grid(row = 5,
                            column = 0, columnspan = 2,
                            sticky= "ns")

        # Goes back to the login screen without registering the user
        backLabel = tk.Label(self,
                          text = "Back",
                          font = ("Arial", 7, "bold", "underline"),
                          fg = "Blue")
        backLabel.bind("<Button-1>", _return)
        backLabel.grid(row = 5,
                       column= 0,
                       sticky = "ew")


class ProfileFrame(tk.Frame):
    def __init__(self, master, controller, userInfo):
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

        def _logoff(*event):
            self.destroy()
            controller.changeFrame("LoginFrame")

        logoff.bind("<Button-1>", _logoff)

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

        self._loadAccounts(self.canvas, self.userInfo)


    def _loadAccounts(self, canvas, userInfo):
        self.accountsHolder = ttk.Frame(canvas)
        canvas.create_window((0, 0), window = self.accountsHolder, anchor = "nw")
        
        for i in range(4):
            self.accountsHolder.columnconfigure(i, minsize = 175)

        self.accounts = {}
        accounts = getAccounts(userInfo[0])
        
        for row, account in enumerate(accounts):
            accountId, plataform, login, password, logo = account[0:5]
            listAccount(accountId, plataform, login, password, logo, row, self.accountsHolder, self)
        
        def _addAccount():
            popup = tk.Toplevel()
            popup.title("Add Account")

            widgets = tk.Frame(popup)
            widgets.pack(anchor = "center")

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
            
            addLoginLabel = tk.Label(widgets, text = "Login:")
            addLoginLabel.grid(row = 1,
                                column = 1)

            addLoginEntry = tk.Entry(widgets)
            addLoginEntry.grid(row = 1,
                                column = 2)
            
            addPasswordLabel = tk.Label(widgets, text = "Password:")
            addPasswordLabel.grid(row = 2,
                                    column = 1)

            addPasswordEntry = tk.Entry(widgets)
            addPasswordEntry.grid(row = 2,
                                    column = 2)
            
            def _saveAccount():
                try:
                    account = [addPlataformEntry.get(), addLoginEntry.get(), addPasswordEntry.get(), _saveAccount.logoBytes, userInfo[0]]
                    cursor.execute("INSERT INTO accounts (plataform, login, password, logo, user_id) VALUES (?, ?, ?, ?, ?)", (account))
                
                except AttributeError:
                    account = [addPlataformEntry.get(), addLoginEntry.get(), addPasswordEntry.get(), userInfo[0]]
                    cursor.execute("INSERT INTO accounts (plataform, login, password, user_id) VALUES (?, ?, ?, ?)", (account))
                connection.commit()
                
                self._reloadAccounts()
                popup.destroy()

            saveButton = tk.Button(widgets,
                                    text = "Add",
                                    command = _saveAccount)
            saveButton.grid(row = 3,
                            column = 0, columnspan = 3)
            
            def _addLogo():
                logoPath = filedialog.askopenfilename()
                logoImg = Image.open(logoPath)
                logoImg.thumbnail((100, 100))
                with open(logoPath, "rb") as file:
                    _saveAccount.logoBytes = file.read()

                logoImg = ImageTk.PhotoImage(logoImg)
                addPlataformLogo.config(image = logoImg)
                addPlataformLogo.image = logoImg

        plusImage = Image.open("assets/Plus_Icon.png")
        plusImage.thumbnail((75, 75))
        plusImage = ImageTk.PhotoImage(plusImage)

        addPlataformButton = tk.Button(self.accountsHolder,
                                        image = plusImage,
                                        command = _addAccount)
        addPlataformButton.grid(column = 1, columnspan = 2,
                                sticky = "s")
        addPlataformButton.image = plusImage
        
        self.accountsHolder.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    def _reloadAccounts(self):
        self.accountsHolder.destroy()
        self._loadAccounts(self.canvas, self.userInfo)



if __name__ == '__main__':
    window = PasswordManager()
    connection = sqlite3.connect("UsersInfo.db")    
    cursor = connection.cursor()

    # Checks if the tables exist in the data base, if they dont, create them
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
    else:
        pass
    
    window.mainloop()
    connection.close()