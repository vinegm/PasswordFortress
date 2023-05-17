import tkinter as tk
from src.utils import *
from src.settings import *
from src.loginframe.utils.changeframe import *


def login_User(username: tk.Entry, password: tk.Entry, guide: tk.Label, connection, window: tk.Tk):
    """Checks if username and password match a user and logs said user

    Parameters:
    username(tk.Entry): Username typed in the login
    password(tk.Entry): Password typed in the login
    guide(tk.Label): Label for giving feedback if the user isn't able to log in
    connection(sqlite3.Connection): Connection to the database
    window(tk.Tk): Window of the app
    """
    user_info = user_exists(username.get(), connection)
    if user_info == False:
        guide.configure(text = INVALID_LOGIN,
                        fg = INVALID_LOGIN_FG)
        return
    
    hashed_password = hash_check(password.get(), user_info[3])
    if hashed_password != user_info[4]:
        guide.configure(text = INVALID_LOGIN,
                        fg = INVALID_LOGIN_FG)
        return

    raise Exception("WIP PROFILE FRAME")
    change_frame()
