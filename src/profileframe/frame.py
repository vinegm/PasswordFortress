import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from io import BytesIO
from src.utils import *


class ProfileFrame(tk.Frame):
    """Frame responsable for registering a user in the app

    Attributes:
    Connection: Database of the app
    master: Widget/window where this frame will be loaded
    controller: Main class of the app
    userInfo (tuple): Contains all the login information of the user

    Methods:
    _loadAccounts: Loads the accounts and widgets from the frame
    _addAccount: Creates a pop-up window for the user to add a account
    _reloadAccounts: Destroy and makes the frame again to reaload it
    _listAccount: Lists the accounts on the frame
    _logoff: Destroys the logged in frame and goes back to the LoginFrame
    """
    def __init__(self, connection, master: tk.Tk, controller):
        tk.Frame.__init__(self, master)
        self.userInfo = [0,0,0,0,0,0,0,0]
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
        """Loads the accounts and widgets from the frame
        
        Parameters:
        connection: Database of the app
        """
        self.accountsHolder = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window = self.accountsHolder, anchor = "nw")
        
        for i in range(4):
            self.accountsHolder.columnconfigure(i, minsize = 175)

        self.accounts = {}
        accounts = get_accounts(self.userInfo[0], connection)
        
        for row, account in enumerate(accounts):
            accountId, plataform, login, password, logo = account[0:5]
            self._listAccount(accountId, plataform, login, password, logo, row, self.accountsHolder, connection)
        
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
        """Creates a pop-up window for the user to add a account
        
        Parameters:
        connection: Used to save the account information to the database
        """
        popup = tk.Toplevel()
        popup.title("Add Account")

        widgets = tk.Frame(popup)
        widgets.pack(anchor = "center")

        def _addLogo():
            """Changes the logo of the new account"""
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
            """Saves the account to the database"""
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
        """Destroy and makes the frame again to reaload it"""
        self.accountsHolder.destroy()
        self._loadAccounts(connection)
    
    def _listAccount(self, accountId, plataform, login, password, logo, frameRow, holder, connection):
        """Lists the accounts on the frame
        
        Parameters:
        accountId: Id of the account in the database
        plataform: Plataform of the account
        login: Login of the account
        password: Password of the account
        logo: Logo of the plataform
        frameRow: Row where the account must be shown
        holder: Frame that holds the widgets
        connection: Database of the app
        """
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
            """Deletes a given account

            Parameters:
            accountId: Id of the account to be deleted
            """
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
            """Edits a existing account
            
            Parameters:
            accountId: Id of the account that will be edited
            """
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
                """Saves the edited account to the database"""
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
            """Changes the logo of a given account
            
            Parameters:
            accountId: Id of the account that will have its logo changed
            """
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
        """Destroys the logged in frame and goes back to the LoginFrame
        
        Parameters:
        controller: Master window, used to call the function changeFrame
        """
        self.destroy()
        controller.changeFrame("LoginFrame")
