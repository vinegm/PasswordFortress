from tkinter import *
import hashlib
import pickle

class userInfo:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.accounts = dict()

    def getAccounts (self):
        return self.accounts()

    def getUsername (self):
        return self.username

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
    except FileNotFoundError:
        return False
                

class PasswordManager (Tk):
    def __init__(self):
        Tk.__init__(self)
        
        framesHolder = Frame(self)
        framesHolder.pack(anchor = "center", fill = "both", expand = True)
        framesHolder.grid_rowconfigure(0, weight = 1)
        framesHolder.grid_columnconfigure(0, weight = 1)
        
        self.frames = {}
        for F in (LoginFrame, RegisterFrame, ProfileFrame):
            page_name = F.__name__
            frame = F(framesHolder, self)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky="nsew")
    
        self.ChangeFrame("LoginFrame")

    def ChangeFrame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class LoginFrame (Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
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

        RegisterLabel = Label(self,
                              text = "Register",
                              font = ("Arial", 7, "bold", "underline"),
                              fg = "Blue")
        RegisterLabel.bind("<Button-1>", lambda event: controller.ChangeFrame("RegisterFrame"))
        RegisterLabel.grid(pady = 5,
                           row = 3,
                           column= 0)
                           #sticky = "ew")

        def _LoginUser(*event):
            if (user := UserExists(username := hashlib.md5(usernameEntry.get().encode()).hexdigest())) == False:
                pass
            elif (password := hashlib.md5(passwordEntry.get().encode()).hexdigest()) != user.password:
                pass
            else:
                print("logado")
            
            #controller.ChangeFrame("ProfileFrame")

        passwordEntry.bind("<Return>", _LoginUser)
        LoginButton = Button(self,
                             text = "Login",
                             command = _LoginUser)
        LoginButton.grid(pady = 10,
                         row = 3,
                         column = 0, columnspan = 2,
                         sticky= "ns")
class RegisterFrame (Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        head = Label(self,
                     text = "Create Your Own Profile!",
                     font = ("Arial", 12, "bold"))
        head.grid(pady = 20,
                  padx = 10,
                  row = 0,
                  column = 0, columnspan = 2,
                  sticky="nsew")

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
        nicknameEntry.bind("<Return>", lambda event: usernameEntry.focus_set())

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

        passwordLabel = Label(self,
                              text = "Password:",
                              font = ("Arial", 9, "bold"))
        passwordLabel.grid(pady = 5,
                           row = 3,
                           column = 0)
        
        passwordEntry = Entry(self, show = "*")
        passwordEntry.grid(pady = 5,
                           row = 3,
                           column = 1)
        passwordEntry.bind("<Return>", lambda event: confirmPasswordEntry.focus_set())

        confirmPasswordLabel = Label(self,
                                     text = "Confirm\nPassword:",
                                     font = ("Arial", 9, "bold"))
        confirmPasswordLabel.grid(pady = 5,
                                  row = 4,
                                  column = 0)
        
        confirmPasswordEntry = Entry(self, show = "*")
        confirmPasswordEntry.grid(pady = 5,
                                  row = 4,
                                  column = 1)
        
        warningLabel = Label(self,
                             font = ("arial", 9, "bold"))

        def _Return(*event):
            controller.ChangeFrame("LoginFrame")
            for selectEntry in (nicknameEntry, usernameEntry, passwordEntry, confirmPasswordEntry):
                selectEntry.delete(0, END)
            warningLabel.config(text = "")

        def _RegisterUser(*event):
            warningLabel.grid(pady = 5,
                              row = 6,
                              column = 0, columnspan = 2,
                              sticky= "nsew")
            
            if nicknameEntry.get() == "" or usernameEntry.get() == "" or \
               passwordEntry.get() == "" or confirmPasswordEntry.get() == "":
                warningLabel.config(text = "Fill All\nThe Boxes!")

            elif UserExists(username := hashlib.md5(usernameEntry.get().encode()).hexdigest()) != False:
                warningLabel.config(text = "Username Unavailable!")

            elif confirmPasswordEntry.get() != passwordEntry.get():
                warningLabel.config(text = "Passwords Don't Match!")

            else:
                password = hashlib.md5(passwordEntry.get().encode()).hexdigest()
                user = userInfo(username, password)
                serializedUser = pickle.dumps(user) + b"\n"
                with open("SavedUsers.users", "ab") as file:
                    file.write(serializedUser)
                    print("usuário salvo!")
                _Return()

        confirmPasswordEntry.bind("<Return>", _RegisterUser)
        RegisterButton = Button(self,
                                text = "Register",
                                command = _RegisterUser)
        RegisterButton.grid(row = 5,
                            column = 0, columnspan = 2,
                            sticky= "ns")

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