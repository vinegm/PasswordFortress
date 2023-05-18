import tkinter as tk
from src.settings import *
from src.utils import *
from src.loginframe.loginuser import *

class LoginFrame(tk.Frame):
    """Frame responsable for login a user in the app

    Attributes:
    Connection(sqlite3.Connection): Database of the app
    master(tk.frame): Frame where this frame will be loaded
    window(tk.Tk): Window of the app
    """
    def __init__(self, connection: sqlite3.Connection, master: tk.Frame, window: tk.Tk):
        tk.Frame.__init__(self, master, bg = BG_APP)

        widgets_holder = tk.Frame(self,
                                  bg = BG_APP)
        widgets_holder.pack(expand = True)

        header = tk.Label(widgets_holder,
                          text = LOGIN_HEADER_TEXT,
                          font = LOGIN_HEADER_FONT,
                          fg = FG,
                          bg = BG_APP)
        header.pack(anchor = "center",
                    pady = 10)

        guide = tk.Label(widgets_holder,
                         text = LOGIN_GUIDE_TEXT,
                         font = LOGIN_WIDGETS_FONT,
                         fg = FG,
                         bg = BG_APP)
        guide.pack(anchor = "center",
                   pady = 10)

        username = tk.Entry(widgets_holder,
                            font = LOGIN_WIDGETS_FONT,
                            fg = HINT_FG,
                            bg = BG_APP)
        username.pack(anchor = "center",
                      pady = 5)
        username.insert(0, LOGIN_USERNAME_HINT)
        username.bind("<FocusIn>", lambda event: entry_focus_in(username, LOGIN_USERNAME_HINT))
        username.bind("<FocusOut>", lambda event: entry_focus_out(username, LOGIN_USERNAME_HINT))
        username.bind("<Return>", lambda event: password.focus())

        password = tk.Entry(widgets_holder,
                            font = LOGIN_WIDGETS_FONT,
                            fg = HINT_FG,
                            bg = BG_APP)
        password.pack(anchor = "center",
                      pady = 5)
        password.insert(0, LOGIN_PASSWORD_HINT)
        password.bind("<FocusIn>", lambda event: entry_focus_in(password, LOGIN_PASSWORD_HINT))
        password.bind("<FocusOut>", lambda event: entry_focus_out(password, LOGIN_PASSWORD_HINT))
        password.bind("<Return>", lambda event: (login_User(username, password, WIDGETS, guide, login, connection, window)))

        WIDGETS = {LOGIN_GUIDE_TEXT: guide,
                   LOGIN_USERNAME_HINT: username,
                   LOGIN_PASSWORD_HINT: password}

        register = tk.Button(widgets_holder,
                             text = LOGIN_REGISTER_TEXT,
                             font = LOGIN_REGISTER_FONT,
                             fg = LOGIN_REGISTER_FG,
                             bg = BG_APP,
                             command = lambda: (window.change_frame("RegisterFrame"), clear_frame(WIDGETS), login.focus()))
        register.configure(relief = tk.FLAT)
        register.pack(anchor = "w",
                      pady = 5)
        
        login = tk.Button(widgets_holder,
                          text = LOGIN_LOG_IN_TEXT,
                          font = LOGIN_WIDGETS_FONT,
                          fg = FG,
                          bg = BG_APP,
                          command = lambda: (login_User(username, password, WIDGETS, guide, login, connection, window)))
        login.pack(anchor = "center")
