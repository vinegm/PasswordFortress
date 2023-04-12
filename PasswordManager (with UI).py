from tkinter import *
import hashlib
import pickle

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

    usernameEntry.focus_set()
    def _FocusPasswordEntry(event):
        passwordEntry.focus_set()
    usernameEntry.bind("<Return>", _FocusPasswordEntry)

    def _Return(event):
        username = usernameEntry.get()
        password = passwordEntry.get()
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