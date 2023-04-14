from tkinter import *
import hashlib
import pickle
# Class responsable to hold the user information
class UserInfo():
    def __init__(self, nickname, username, password):
        self.nickname = nickname
        self.username = username
        self.password = password
        self.accounts = dict()

    def getAccounts (self):
        return self.accounts()


# Checks if a user exists in the .users, if not, returns False, if it does it returns the line the user is in
def userExists(search):
    userLine = 0
    try:
        with open("SavedUsers.users", "rb") as file:
            for line in file.readlines():
                serializedUser = line.rstrip()
                lookingForUser = pickle.loads(serializedUser)
                if lookingForUser.username == search:
                    return lookingForUser
                userLine += 1
        return False
    # Returns False if the file does not exist
    except FileNotFoundError:
        return False

          
# Class responsable to loading the frames and app
class PasswordManager(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.title("Password Manager")
        self.geometry("300x250")
        self.eval("tk::PlaceWindow . center")
        
        framesHolder = Frame(self)
        framesHolder.pack(anchor = "center")
        
        self.frames = {}
        for F in (LoginFrame, RegisterFrame, ProfileFrame):
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
class LoginFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.columnconfigure(0, minsize=100)
        self.columnconfigure(1, minsize=200)
        # Header label
        head = Label(self,
                     text = "Welcome to a Password Manager!",
                     font = ("Arial", 12, "bold"))
        head.grid(pady = 20,
                  padx = 10,
                  row = 0,
                  column = 0, columnspan = 2,
                  sticky="nsew")

        # Username label and entry
        usernameLabel = Label(self,
                              text = "Username:",
                              font = ("Arial", 9, "bold"))
        usernameLabel.grid(pady = 5,
                           row = 1,
                           column = 0,
                           sticky = "e")

        usernameEntry = Entry(self)
        usernameEntry.grid(pady = 5,
                           row = 1,
                           column = 1,
                           sticky = "w")
        
        # Bind to set focus on the password entry once username is entered
        usernameEntry.bind("<Return>", lambda event: passwordEntry.focus_set())

        # Password label and entry
        passwordLabel = Label(self,
                              text = "Password:",
                              font = ("Arial", 9, "bold"))
        passwordLabel.grid(pady = 5,
                           row = 2,
                           column = 0,
                           sticky = "e")

        passwordEntry = Entry(self, show = "*")
        passwordEntry.grid(pady = 5,
                           row = 2,
                           column = 1,
                           sticky = "w")

        def _changeAndClearFrame(nextFrame):
            for selectEntry in (usernameEntry, passwordEntry):
                selectEntry.delete(0, END)
            head.config(text = "Welcome to a Password Manager!")
            controller.changeFrame(nextFrame)

        # Register label and entry, responsable for sending the user to a register screen if needed
        RegisterLabel = Label(self,
                              text = "Register",
                              font = ("Arial", 7, "bold", "underline"),
                              fg = "Blue")
        RegisterLabel.bind("<Button-1>", lambda event: _changeAndClearFrame("RegisterFrame")) 
        RegisterLabel.grid(pady = 5,
                           row = 3,
                           column= 0)

        # Function responsable for checking if the user and password are registered in the system and login
        def _loginUser (*event):
            if (user := userExists(hashlib.md5(usernameEntry.get().encode()).hexdigest())) == False:
                head.config(text = "Username/Password Incorrect!")

            elif hashlib.md5(passwordEntry.get().encode()).hexdigest() != user.password:
                head.config(text = "Username/Password Incorrect!")
                
            else:
                _changeAndClearFrame("ProfileFrame")

        # Button and bind responsable for calling the login function
        passwordEntry.bind("<Return>", _loginUser)
        LoginButton = Button(self,
                             text = "Login",
                             command = _loginUser)
        LoginButton.grid(pady = 10,
                         row = 3,
                         column = 0, columnspan = 2,
                         sticky= "ns")


# Class responsable for the register screen
class RegisterFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.columnconfigure(0, minsize=100)
        self.columnconfigure(1, minsize=200)
        # Header Label
        head = Label(self,
                     text = "Register an Account!",
                     font = ("Arial", 12, "bold"))
        head.grid(pady = 20,
                  padx = 10,
                  row = 0,
                  column = 0, columnspan = 2,
                  sticky="nsew")
        
        # Nickname label and entry
        nicknameLabel = Label(self,
                              text = "Nickname:",
                              font = ("Arial", 9, "bold"))
        nicknameLabel.grid(pady = 5,
                           row = 1,
                           column = 0,
                           sticky = "e")
        
        nicknameEntry = Entry(self)
        nicknameEntry.grid(pady = 5,
                           row = 1,
                           column = 1,
                           sticky = "w")
        
        # Set focus to next box
        nicknameEntry.bind("<Return>", lambda event: usernameEntry.focus_set())

        # Username label and entry
        usernameLabel = Label(self,
                              text = "Username:",
                              font = ("Arial", 9, "bold"))
        usernameLabel.grid(pady = 5,
                           row = 2,
                           column = 0,
                           sticky = "e")
        
        usernameEntry = Entry(self)
        usernameEntry.grid(pady = 5,
                           row = 2,
                           column = 1,
                           sticky = "w")
        usernameEntry.bind("<Return>", lambda event: passwordEntry.focus_set())

        # Password label and entry
        passwordLabel = Label(self,
                              text = "Password:",
                              font = ("Arial", 9, "bold"))
        passwordLabel.grid(pady = 5,
                           row = 3,
                           column = 0,
                           sticky = "e")
        
        passwordEntry = Entry(self, show = "*")  # Password box only shows * insted of the password
        passwordEntry.grid(pady = 5,
                           row = 3,
                           column = 1,
                           sticky = "w")
        passwordEntry.bind("<Return>", lambda event: confirmPasswordEntry.focus_set())

        # Password Confirmation label and entry
        confirmPasswordLabel = Label(self,
                                     text = "Confirm\nPassword:",
                                     font = ("Arial", 9, "bold"))
        confirmPasswordLabel.grid(pady = 5,
                                  row = 4,
                                  column = 0,
                                  sticky = "e")
        
        confirmPasswordEntry = Entry(self, show = "*")  # Password confirmation box only shows *
        confirmPasswordEntry.grid(pady = 5,
                                  row = 4,
                                  column = 1,
                                  sticky = "w")

        # Returns to the login screen and clears all the entrys in the register screen
        def _return(*event):
            controller.changeFrame("LoginFrame")
            for selectEntry in (nicknameEntry, usernameEntry, passwordEntry, confirmPasswordEntry):
                selectEntry.delete(0, END)
            head.config(text = "Register an Account!")

        # Registers the user
        def _registerUser(*event):
            # If a box is left empty
            if nicknameEntry.get() == "" or usernameEntry.get() == "" or \
               passwordEntry.get() == "" or confirmPasswordEntry.get() == "":
                head.config(text = "Fill All The Boxes!")

            # If a username is already in use
            elif userExists(username := hashlib.md5(usernameEntry.get().encode()).hexdigest()) != False:
                head.config(text = "Username Unavailable!")

            # If password and the password confirmation dont match
            elif confirmPasswordEntry.get() != passwordEntry.get():
                head.config(text = "Passwords Don't Match!")

            # Registers the user if everything is ok
            else:
                nickname = nicknameEntry.get()
                password = hashlib.md5(passwordEntry.get().encode()).hexdigest()
                user = UserInfo(nickname, username, password)
                serializedUser = pickle.dumps(user) + b"\n"
                with open("SavedUsers.users", "ab") as file:
                    file.write(serializedUser)
                _return()

        # Button and bind responsable for calling the register function
        confirmPasswordEntry.bind("<Return>", _registerUser)
        RegisterButton = Button(self,
                                text = "Register",
                                command = _registerUser)
        RegisterButton.grid(row = 5,
                            column = 0, columnspan = 2,
                            sticky= "ns")

        # Goes back to the login screen without registering the user
        backLabel = Label(self,
                          text = "Back",
                          font = ("Arial", 7, "bold", "underline"),
                          fg = "Blue")
        backLabel.bind("<Button-1>", _return)
        backLabel.grid(row = 5,
                       column= 0,
                       sticky = "ew")


class ProfileFrame(Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        #print(user.username)


if __name__ == '__main__':
    window = PasswordManager()
    window.resizable(False, False)
    window.mainloop()