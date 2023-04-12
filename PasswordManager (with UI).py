from tkinter import *
import hashlib
import pickle


def RegisterFrame():

    def RegisterUser(username, password):
        raise Exception("Code Missing!")

    def CheckForExistingUser(Username):
        raise Exception("Code Missing!")

    raise Exception("Code Missing!")

def LoginFrame(master):
    LoginFrame = Frame(master)
    LoginFrame.pack(anchor="center")

    # Head label
    head = Label(LoginFrame,
                 text = "Welcome to a Password Manager!",
                 font = ("Arial", 12, "bold"))
    head.grid(row = 0,
              column = 0, columnspan = 2,
              sticky="nsew")

    # Username label and entry
    usernameLabel = Label(LoginFrame,
                          text = "Username:",
                          font = ("Arial", 9, "bold"))
    usernameLabel.grid(pady = 15,
                       row = 1,
                       column = 0)

    usernameEntry = Entry(LoginFrame)
    usernameEntry.grid(pady = 15,
                       row = 1,
                       column = 1)

    # Password label and entry
    passwordLabel = Label(LoginFrame,
                          text = "Password:",
                          font = ("Arial", 9, "bold"))
    passwordLabel.grid(row = 2,
                       column = 0)

    passwordEntry = Entry(LoginFrame)
    passwordEntry.grid(row = 2,
                       column = 1)

    def _GoToRegisterFrame(event):
        raise Exception("Code Missing!")

    # Label to change frame so the user can register a new profile
    notRegistered = Label(LoginFrame,
                          text = "Register",
                          font = ("Arial", 9, "bold", "underline"),
                          fg = "Blue")
    notRegistered.bind("<Button-1>", _GoToRegisterFrame)
    notRegistered.grid(pady = 5,
                       row = 3,
                       column= 0,
                       sticky = "w")

    # Set focus to the username entry and then to the password entry
    usernameEntry.focus_set()
    def _FocusPasswordEntry(event):
        passwordEntry.focus_set()
    usernameEntry.bind("<Return>", _FocusPasswordEntry)

    # Returns the username and password
    def _LoginUser(event):
        username = hashlib.md5(usernameEntry.get().encode()).hexdigest()
        password = hashlib.md5(passwordEntry.get().encode()).hexdigest()
        print(f"user: {username}")
        print(f"password: {password}")
        
        raise Exception("Missing Code!")
    passwordEntry.bind("<Return>", _LoginUser)
    

if __name__ == "__main__":
    window = Tk()
    window.geometry("750x250")
    window.title("Password Manager")
    LoginFrame(window)

    window.mainloop()

print("finalizado")