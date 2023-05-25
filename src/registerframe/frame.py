import tkinter as tk
from src.utils import *
from src.settings import *
from src.registerframe.registeruser import *


class RegisterFrame(tk.Frame):
    """Frame responsable for registering a user in the app

    Attributes:
    Connection(sqlite3.Connection): Database of the app
    master(tk.Frame): Frame where this frame will be loaded
    window(tk.Tk): Window of the app
    """
    def __init__(self, connection: sqlite3.Connection, master: tk.Frame, window: tk.Tk):
        tk.Frame.__init__(self, master, bg = BG_APP)

        widgets_holder = tk.Frame(self,
                                  bg = BG_APP)
        widgets_holder.pack(expand = True)

        header = tk.Label(widgets_holder,
                          text = REGISTER_HEADER_TEXT,
                          font = REGISTER_HEADER_FONT,
                          fg = FG,
                          bg = BG_APP)
        header.pack(anchor = "center",
                    pady = 10)

        guide = tk.Label(widgets_holder,
                         text = REGISTER_GUIDE_TEXT,
                         font = REGISTER_WIDGETS_FONT,
                         fg = FG,
                         bg = BG_APP)
        guide.pack(anchor = "center",
                   pady = 10)

        entrys_holder = tk.Frame(widgets_holder,
                                 bg = BG_APP)
        entrys_holder.pack(expand = True)

        nickname = tk.Entry(entrys_holder,
                            font = REGISTER_WIDGETS_FONT,
                            fg = HINT_FG,
                            bg = BG_APP)
        nickname.pack(anchor = "center",
                      pady = 5)
        nickname.insert(0, REGISTER_NICKNAME_HINT)
        nickname.bind("<FocusIn>", lambda event: entry_focus_in(nickname, REGISTER_NICKNAME_HINT))
        nickname.bind("<FocusOut>", lambda event: entry_focus_out(nickname, REGISTER_NICKNAME_HINT))
        nickname.bind("<Return>", lambda event: username.focus())

        username = tk.Entry(entrys_holder,
                            font = REGISTER_WIDGETS_FONT,
                            fg = HINT_FG,
                            bg = BG_APP)
        username.pack(anchor = "center",
                      pady = 5)
        username.insert(0, REGISTER_USERNAME_HINT)
        username.bind("<FocusIn>", lambda event: entry_focus_in(username, REGISTER_USERNAME_HINT))
        username.bind("<FocusOut>", lambda event: entry_focus_out(username, REGISTER_USERNAME_HINT))
        username.bind("<Return>", lambda event: password.focus())

        password = tk.Entry(entrys_holder,
                            font = REGISTER_WIDGETS_FONT,
                            fg = HINT_FG,
                            bg = BG_APP)
        password.pack(anchor = "center",
                      pady = 5)
        password.insert(0, REGISTER_PASSWORD_HINT)
        password.bind("<FocusIn>", lambda event: entry_focus_in(password, REGISTER_PASSWORD_HINT))
        password.bind("<FocusOut>", lambda event: entry_focus_out(password, REGISTER_PASSWORD_HINT))
        password.bind("<Return>", lambda event: confirm_password.focus())

        bar_frame = create_strength_bar(password, entrys_holder)
        bar_frame.pack(anchor = "nw",
                       fill = "x")

        confirm_password = tk.Entry(entrys_holder,
                                    font = REGISTER_WIDGETS_FONT,
                                    fg = HINT_FG,
                                    bg = BG_APP)
        confirm_password.pack(anchor = "center",
                              pady = 5)
        confirm_password.insert(0, REGISTER_CONFIRM_PASSWORD_HINT)
        confirm_password.bind("<FocusIn>", lambda event: entry_focus_in(confirm_password, REGISTER_CONFIRM_PASSWORD_HINT))
        confirm_password.bind("<FocusOut>", lambda event: entry_focus_out(confirm_password, REGISTER_CONFIRM_PASSWORD_HINT))
        confirm_password.bind("<Return>", lambda event: (back.focus(), register_user(nickname, username, password, confirm_password, WIDGETS, guide, connection)))
        
        WIDGETS = {REGISTER_GUIDE_TEXT: guide,
                   REGISTER_NICKNAME_HINT: nickname,
                   REGISTER_USERNAME_HINT: username,
                   REGISTER_PASSWORD_HINT: password,
                   REGISTER_CONFIRM_PASSWORD_HINT: confirm_password}

        back = tk.Button(widgets_holder,
                         text = REGISTER_BACK_TEXT,
                         font = REGISTER_BACK_FONT,
                         fg = REGISTER_BACK_FG,
                         bg = BG_APP,
                         command = lambda: (window.change_frame("LoginFrame"), clear_frame(WIDGETS)))
        back.configure(relief = tk.FLAT)
        back.pack(anchor = "w",
                  pady = 5)
        
        register = tk.Button(widgets_holder,
                             text = REGISTER_SING_UP_TEXT,
                             font = REGISTER_WIDGETS_FONT,
                             fg = FG,
                             bg = BG_APP,
                             command = lambda: register_user(nickname, username, password, confirm_password, WIDGETS, guide, connection))
        register.pack(anchor = "center")
