from tkinter import *
import hashlib
import pickle

def LoginRegisterFrame(master):
    LoginRegisterFrame = Frame(master)
    LoginRegisterFrame.pack(anchor="center")

    # Label and entry for Login/Register

    # Username label and entry
    usernameLabel = Label(LoginRegisterFrame,
                   text = "Usuário: ")
    usernameLabel.grid(row=0, column=0)

    userEntry = Entry(LoginRegisterFrame)
    userEntry.grid(pady=15, row=0, column=1)

    # Password label and entry
    passwordLabel = Label(LoginRegisterFrame,
                   text = "Senha: ")
    passwordLabel.grid(row=1, column=0)

    passwordEntry = Entry(LoginRegisterFrame)
    passwordEntry.grid(row=1, column=1)



window = Tk()
window.title("Password Manager")
LoginRegisterFrame(window)

window.mainloop()

print("finalizado")