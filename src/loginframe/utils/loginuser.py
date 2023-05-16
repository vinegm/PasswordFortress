import tkinter as tk
from src.utils import *
from src.loginframe.utils.changeframe import *


def login_User(username: tk.Entry, password: tk.Entry, connection, window: tk.Tk):
    """Checks if username and password match a user and logs said user

    Parameters:
    username(tk.Entry): Username typed in the login
    password(tk.Entry): Password typed in the login
    connection(sqlite3.Connection): Connection to the database
    window(tk.Tk): Window of the app
    """
    user_info = user_exists(username.get(), connection)
    if user_info == False:
        print("INCORRECT")
        return
    
    hashed_password = hash_check(password.get(), user_info[3])
    if hashed_password != user_info[4]:
        print("INCORRECT")
        return

    print("SUCESS")
    raise Exception("WIP, NOT ABLE TO CHANGE FRAME")
    change_frame()
