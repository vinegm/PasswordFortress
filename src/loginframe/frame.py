import tkinter as tk
from src.settings import *
from src.utils import *
from src.profileframe import *
from src.loginframe.utils import *

class LoginFrame(tk.Frame):
    """Frame responsable for login a user in the app

    Attributes:
    Connection(sqlite3.Connection): Database of the app
    master(tk.frame): Frame where this frame will be loaded
    window(tk.Tk): Window of the app
    """
    def __init__(self, connection: sqlite3.Connection, master: tk.Frame, profile_frame: ProfileFrame, window: tk.Tk):
        tk.Frame.__init__(self, master, bg = BG_APP)

        widgets_holder = tk.Frame(self,
                                  bg = BG_APP)
        widgets_holder.pack(expand = True)

        header = tk.Label(widgets_holder,
                          text = "Welcome to PasswordFortress!",
                          font = ("Arial", 12, "bold"),
                          fg = FG,
                          bg = BG_APP)
        header.pack(anchor = "center",
                    pady = 10)

        username = tk.Entry(widgets_holder,
                            font = ("Arial", 12),
                            fg = HINT_FG,
                            bg = BG_APP)
        username.pack(anchor = "center",
                      pady = 5)
        USERNAME_HINT = "Enter Your Username"
        username.insert(0, USERNAME_HINT)
        username.bind('<FocusIn>', lambda event: entry_focus_in(username, USERNAME_HINT))
        username.bind('<FocusOut>', lambda event: entry_focus_out(username, USERNAME_HINT))

        password = tk.Entry(widgets_holder,
                            font = ("Arial", 12),
                            fg = HINT_FG,
                            bg = BG_APP)
        password.pack(anchor = "center",
                      pady = 5)
        PASSWORD_HINT = "Enter Your Password"
        password.insert(0, PASSWORD_HINT)
        password.bind('<FocusIn>', lambda event: entry_focus_in(password, PASSWORD_HINT))
        password.bind('<FocusOut>', lambda event: entry_focus_out(password, PASSWORD_HINT))

        login = tk.Button(widgets_holder,
                          text = "Login",
                          font = ("Arial", 12),
                          fg = FG,
                          bg = BG_APP,
                          command = lambda: login_User(username, password, connection, window))
        login.pack(anchor = "center",
                   pady = 10)
        
        register = tk.Button(widgets_holder,
                          text = "register",
                          font = ("Arial", 12),
                          fg = FG,
                          bg = BG_APP)
                          #command = lambda: register_User(username, password, connection, window))
        register.pack(anchor = "center",
                   pady = 10)
