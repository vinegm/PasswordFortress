from tkinter import *
import hashlib
import pickle
# Class responsable to hold the user information
class userInfo:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.accounts = dict()

    def getAccounts (self):
        return self.accounts()

# Checks if a user exists in the .users, if not, returns False, if it does it returns the line the user is in
def UserExists(search):
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
class PasswordManager (Tk):
    def __init__(self):
        Tk.__init__(self)
        
        framesHolder = Frame(self)
        framesHolder.pack(anchor = "center",
                          fill = "both",
                          expand = True)
        framesHolder.grid_rowconfigure(0, weight = 1)
        framesHolder.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}
        for F in (LoginFrame, RegisterFrame, ProfileFrame):
            page_name = F.__name__
            frame = F(framesHolder, self)
            self.frames[page_name] = frame
            frame.grid(row = 0,
                       column = 0,
                       sticky = "nsew")
    
        self.ChangeFrame("LoginFrame")

    # Function responsable for changing the frames, loading one on top of another
    def ChangeFrame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# Class responsable for the login screen
class LoginFrame (Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
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

        # Register label and entry, responsable for sending the user to a register screen if needed
        RegisterLabel = Label(self,
                              text = "Register",
                              font = ("Arial", 7, "bold", "underline"),
                              fg = "Blue")
        RegisterLabel.bind("<Button-1>", lambda event: controller.ChangeFrame("RegisterFrame"))
        RegisterLabel.grid(pady = 5,
                           row = 3,
                           column= 0)
                           #sticky = "ew")

        # Function responsable for checking if the user and password are registered in the system and login
        def _LoginUser(*event):
            warningLabel = Label(self,
                                 font = ("arial", 9, "bold"))
            warningLabel.grid(pady = 5,
                              row = 4,
                              column = 0, columnspan = 2,
                              sticky= "nsew")
            if (user := UserExists(hashlib.md5(usernameEntry.get().encode()).hexdigest())) == False:
                warningLabel.config(text = "Username/Password Incorrect!")
            elif hashlib.md5(passwordEntry.get().encode()).hexdigest() != user.password:
                warningLabel.config(text = "Username/Password Incorrect!")
            else:
                controller.ChangeFrame("ProfileFrame")
                for selectEntry in (usernameEntry, passwordEntry):
                    selectEntry.delete(0, END)
                warningLabel.config(text = "")
        # Button and bind responsable for calling the login function
        passwordEntry.bind("<Return>", _LoginUser)
        LoginButton = Button(self,
                             text = "Login",
                             command = _LoginUser)
        LoginButton.grid(pady = 10,
                         row = 3,
                         column = 0, columnspan = 2,
                         sticky= "ns")

# Class responsable for the register screen
class RegisterFrame (Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        # Header Label
        head = Label(self,
                     text = "Create Your Own Profile!",
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
                           column = 0)
        
        nicknameEntry = Entry(self)
        nicknameEntry.grid(pady = 5,
                           row = 1,
                           column = 1)
        
        # Set focus to next box
        nicknameEntry.bind("<Return>", lambda event: usernameEntry.focus_set())

        # Username label and entry
        usernameLabel = Label(self,
                              text = "Username:",
                              font = ("Arial", 9, "bold"))
        usernameLabel.grid(pady = 5,
                           row = 2,
                           column = 0)
        
        usernameEntry = Entry(self)
        usernameEntry.grid(pady = 5,
                           row = 2,
                           column = 1)
        usernameEntry.bind("<Return>", lambda event: passwordEntry.focus_set())

        # Password label and entry
        passwordLabel = Label(self,
                              text = "Password:",
                              font = ("Arial", 9, "bold"))
        passwordLabel.grid(pady = 5,
                           row = 3,
                           column = 0)
        
        passwordEntry = Entry(self, show = "*") # Password box only shows * insted of the password
        passwordEntry.grid(pady = 5,
                           row = 3,
                           column = 1)
        passwordEntry.bind("<Return>", lambda event: confirmPasswordEntry.focus_set())

        # Password Confirmation label and entry
        confirmPasswordLabel = Label(self,
                                     text = "Confirm\nPassword:",
                                     font = ("Arial", 9, "bold"))
        confirmPasswordLabel.grid(pady = 5,
                                  row = 4,
                                  column = 0)
        
        confirmPasswordEntry = Entry(self, show = "*") # Password confirmation box only shows *
        confirmPasswordEntry.grid(pady = 5,
                                  row = 4,
                                  column = 1)
        
        # Pre loads the warning label
        warningLabel = Label(self,
                             font = ("arial", 9, "bold"))

        # Returns to the login screen and clears all the entrys in the register screen
        def _Return(*event):
            controller.ChangeFrame("LoginFrame")
            for selectEntry in (nicknameEntry, usernameEntry, passwordEntry, confirmPasswordEntry):
                selectEntry.delete(0, END)
            warningLabel.config(text = "")

        # Registers the user
        def _RegisterUser(*event):
            warningLabel.grid(pady = 5,
                              row = 6,
                              column = 0, columnspan = 2,
                              sticky= "nsew")
            
            # If a box is left empty
            if nicknameEntry.get() == "" or usernameEntry.get() == "" or \
               passwordEntry.get() == "" or confirmPasswordEntry.get() == "":
                warningLabel.config(text = "Fill All\nThe Boxes!")

            # If a username is already in use
            elif UserExists(username := hashlib.md5(usernameEntry.get().encode()).hexdigest()) != False:
                warningLabel.config(text = "Username Unavailable!")

            # If password and the password confirmation dont match
            elif confirmPasswordEntry.get() != passwordEntry.get():
                warningLabel.config(text = "Passwords Don't Match!")

            # Registers the user if everything is ok
            else:
                password = hashlib.md5(passwordEntry.get().encode()).hexdigest()
                user = userInfo(username, password)
                serializedUser = pickle.dumps(user) + b"\n"
                with open("SavedUsers.users", "ab") as file:
                    file.write(serializedUser)
                _Return()

        # Button and bind responsable for calling the register function
        confirmPasswordEntry.bind("<Return>", _RegisterUser)
        RegisterButton = Button(self,
                                text = "Register",
                                command = _RegisterUser)
        RegisterButton.grid(row = 5,
                            column = 0, columnspan = 2,
                            sticky= "ns")

        # Goes back to the login screen without registering the user
        backLabel = Label(self,
                          text = "Back",
                          font = ("Arial", 7, "bold", "underline"),
                          fg = "Blue")
        backLabel.bind("<Button-1>", _Return)
        backLabel.grid(row = 5,
                       column= 0,
                       sticky = "ew")

class ProfileFrame (Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        # raise Exception("Missing Code!")



if __name__ == '__main__':
    window = PasswordManager()
    window.mainloop()