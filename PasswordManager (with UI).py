from tkinter import *
import hashlib
import pickle

def CheckForExistingUser(Username):
    raise Exception("Code Missing!")
    pass

def RegisterUser(username, password):
    raise Exception("Code Missing!")
    pass

def Login(username, password):
    raise Exception("Code Missing!")
    pass

def LoginRegisterFrame(master):
    LoginRegisterFrame = Frame(master)
    LoginRegisterFrame.pack(anchor="center")

    # Username label and entry
    usernameLabel = Label(LoginRegisterFrame,
                          text = "Usuário: ")
    usernameLabel.grid(row=0, column=0)

    usernameEntry = Entry(LoginRegisterFrame)
    usernameEntry.grid(pady=25, row=0, column=1)

    # Password label and entry
    passwordLabel = Label(LoginRegisterFrame,
                          text = "Senha: ")
    passwordLabel.grid(row=1, column=0)

    passwordEntry = Entry(LoginRegisterFrame)
    passwordEntry.grid(row=1, column=1)

    # Set focus to the username entry and then to the password entry
    usernameEntry.focus_set()
    def _FocusPasswordEntry(event):
        passwordEntry.focus_set()
    usernameEntry.bind("<Return>", _FocusPasswordEntry)

    # Returns the username and password
    def _Return(event):
        username = hashlib.md5(usernameEntry.get().encode()).hexdigest()
        password = hashlib.md5(passwordEntry.get().encode()).hexdigest()
        print(f"user: {username}")
        print(f"password: {password}")
    passwordEntry.bind("<Return>", _Return)
    

if __name__ == "__main__":
    window = Tk()
    window.geometry("750x250")
    window.title("Password Manager")
    LoginRegisterFrame(window)

    window.mainloop()

print("finalizado")