import tkinter as tk
from src.utils import *
from src.settings import *
from src.loginframe.timeout import *


def login_User(username_entry: tk.Entry, password_entry: tk.Entry, widgets: dict, guide: tk.Label, login: tk.Button, connection, window: tk.Tk):
    """Checks if username and password match a user and logs said user

    Parameters:
    username(tk.Entry): Entry holding the username of the user
    password(tk.Entry): Entry holding the password of the user
    widgets(dict): Dict cointeining the widgets of the frame for clearing
    guide(tk.Label): Label for giving feedback for the user
    login(tk.Button): Button to log in the account
    connection(sqlite3.Connection): Connection to the database
    window(tk.Tk): Window of the app
    """
    username, password = username_entry.get(), password_entry.get()

    user_info = user_exists(username, connection)
    if user_info == False:
        guide.configure(text = INVALID_LOGIN,
                        fg = INVALID_LOGIN_FG)
        return

    timeout_duration = check_timeout(user_info[0], user_info[7], connection)
    if timeout_duration != None:
        guide.configure(text = f"{TIMEOUT_LOGIN} {timeout_duration}",
                        fg = TIMEOUT_LOGIN_FG)
        return

    hashed_password = hash_wsalt(password, user_info[3])
    if hashed_password != user_info[4]:
        tries_left = failed_login(user_info[0], user_info[5], user_info[6], connection)

        if tries_left > 0:
            guide.configure(text = f"{START_TIMEOUT_WARNING} {tries_left} {END_TIMEOUT_WARNING}",
                            fg = TIMEOUT_WARNING_FG)
            return
        
        guide.configure(text = SUSPENDED_LOGIN,
                        fg = SUSPENDED_LOGIN_FG)
        return

    guide.configure(text = VALID_LOGIN,
                    fg = VALID_LOGIN_FG)

    clear_tries(user_info[0], connection)

    key = KDF(password, user_info[3])
    
    # Passes the user info into the profile frame
    window.frames["ProfileFrame"].user = [user_info[0], user_info[1], user_info[3], user_info[4], key]
    window.frames["ProfileFrame"].reload(True)

    login.focus()
    clear_frame(widgets)

    window.change_frame("ProfileFrame")
