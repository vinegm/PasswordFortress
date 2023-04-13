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
    with open("SavedUsers.users", "rb") as file:
        for line in (editUser := file.readlines()):
            serializedUser = line.rstrip()
            lookingForUser = pickle.loads(serializedUser)
            if lookingForUser.username == search:
                return True
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
        head.grid(row = 0,
                  column = 0, columnspan = 2,
                  sticky="nsew")

        # Username label and entry
        usernameLabel = Label(self,
                              text = "Username:",
                              font = ("Arial", 9, "bold"))
        usernameLabel.grid(pady = 15,
                           row = 1,
                           column = 0)

        usernameEntry = Entry(self)
        usernameEntry.grid(pady = 15,
                           row = 1,
                           column = 1)
        usernameEntry.bind("<Return>", lambda event: passwordEntry.focus_set())

        # Password label and entry
        passwordLabel = Label(self,
                              text = "Password:",
                              font = ("Arial", 9, "bold"))
        passwordLabel.grid(row = 2,
                        column = 0)

        passwordEntry = Entry(self)
        passwordEntry.grid(row = 2,
                           column = 1)

        notRegistered = Label(self,
                              text = "Register",
                              font = ("Arial", 9, "bold", "underline"),
                              fg = "Blue")
        notRegistered.bind("<Button-1>", lambda event: controller.ChangeFrame("RegisterFrame"))
        notRegistered.grid(pady = 5,
                           row = 3,
                           column= 0,
                           sticky = "w")

        def _LoginUser(event):
            username = hashlib.md5(usernameEntry.get().encode()).hexdigest()
            password = hashlib.md5(passwordEntry.get().encode()).hexdigest()
            print(f"user: {username}")
            print(f"password: {password}")
            
            controller.ChangeFrame("ProfileFrame")    
        passwordEntry.bind("<Return>", _LoginUser)
class RegisterFrame (Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        
        head = Label(self,
                     text = "Create Your Own Profile!",
                     font = ("Arial", 12, "bold"))
        head.grid(row = 0,
                  column = 0, columnspan = 2,
                  sticky="nsew")

        nicknameLabel = Label(self,
                              text = "Nickname:",
                              font = ("Arial", 9, "bold"))
        nicknameLabel.grid(row = 1,
                       column = 0)
        
        nicknameEntry = Entry(self)
        nicknameEntry.grid(row = 1,
                       column = 1)
        nicknameEntry.bind("<Return>", lambda event: usernameEntry.focus_set())

        usernameLabel = Label(self,
                              text = "Username:",
                              font = ("Arial", 9, "bold"))
        usernameLabel.grid(row = 2,
                           column = 0)
        
        usernameEntry = Entry(self)
        usernameEntry.grid(row = 2,
                           column = 1)
        usernameEntry.bind("<Return>", lambda event: passwordEntry.focus_set())

        passwordLabel = Label(self,
                              text = "Password:",
                              font = ("Arial", 9, "bold"))
        passwordLabel.grid(row = 3,
                           column = 0)
        
        passwordEntry = Entry(self)
        passwordEntry.grid(row = 3,
                           column = 1)
        passwordEntry.bind("<Return>", lambda event: confirmPasswordEntry.focus_set())

        confirmPasswordLabel = Label(self,
                                     text = "Confirm\nPassword:",
                                     font = ("Arial", 9, "bold"))
        confirmPasswordLabel.grid(row = 4,
                                  column = 0)
        
        confirmPasswordEntry = Entry(self)
        confirmPasswordEntry.grid(row = 4,
                                  column = 1)
        
        def _RegisterUser(event):
            username = hashlib.md5(usernameEntry.get().encode()).hexdigest()
            password = hashlib.md5(passwordEntry.get().encode()).hexdigest()
            if UserExists(username):
                print("toma no cu")
            elif hashlib.md5(confirmPasswordEntry.get().encode()).hexdigest() != password:
                print("toma no cu²")
            else:
                user = userInfo(username, password)
                serializedUser = pickle.dumps(user) + b"\n"
                with open("SavedUsers.users", "ab") as file:
                    file.write(serializedUser)
                    print("usuário salvo!")
                controller.ChangeFrame("LoginFrame")
        confirmPasswordEntry.bind("<Return>", _RegisterUser)


class ProfileFrame (Frame):
    def __init__(self, master, controller):
        Frame.__init__(self, master)



if __name__ == '__main__':
    window = PasswordManager()
    window.mainloop()