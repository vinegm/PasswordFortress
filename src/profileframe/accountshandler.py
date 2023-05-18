import tkinter as tk
from src.settings import *
from src.utils import *


def populate_accounts(master: tk.Frame, user_id: int, connection) -> tk.Frame:
    """Populates the profile frame with the users accounts
    
    Parameters:
    master(tk.Frame): Frame that will hold the widgets
    user_id(int): Id of the current user
    connection(sqlite3.Connection): Connection to the database

    Returns:
    accounts_holder(tk.Frame): Frame containing all the widgets from the user accounts
    """
    if user_id == None:
        return None
    
    accounts_data = get_accounts(user_id, connection)

    for i, account in enumerate(accounts_data):
        print(account)
    
    accounts_holder = tk.Frame(master, bg = BG_APP)
    return accounts_holder


def add_account(profile_frame: tk.Frame, connection) -> None:
    """Creates a popup for the user to add a new account
    
    Parameters:
    profile_frame(tk.Frame): Master frame, used for calling functions
    connection(sqlite3.Connection): Connection to the database
    """
    popup = tk.Toplevel(bg = BG_APP)

    plataform = tk.Entry(popup,
                         font = PROFILE_WIDGETS_FONT,
                         fg = HINT_FG,
                         bg = BG_APP)
    plataform.pack(anchor = "center")
    plataform.insert(0, PROFILE_NEW_PLATAFORM_HINT)
    plataform.bind("<FocusIn>", lambda event: entry_focus_in(plataform, PROFILE_NEW_PLATAFORM_HINT))
    plataform.bind("<FocusOut>", lambda event: entry_focus_out(plataform, PROFILE_NEW_PLATAFORM_HINT))
    plataform.bind("<Return>", lambda event: login.focus())

    login = tk.Entry(popup,
                     font = PROFILE_WIDGETS_FONT,
                     fg = HINT_FG,
                     bg = BG_APP)
    login.pack(anchor = "center")
    login.insert(0, PROFILE_NEW_LOGIN_HINT)
    login.bind("<FocusIn>", lambda event: entry_focus_in(login, PROFILE_NEW_LOGIN_HINT))
    login.bind("<FocusOut>", lambda event: entry_focus_out(login, PROFILE_NEW_LOGIN_HINT))
    login.bind("<Return>", lambda event: password.focus())

    password = tk.Entry(popup,
                        font = PROFILE_WIDGETS_FONT,
                        fg = HINT_FG,
                        bg = BG_APP)
    password.pack(anchor = "center")
    password.insert(0, PROFILE_NEW_PASSWORD_HINT)
    password.bind("<FocusIn>", lambda event: entry_focus_in(password, PROFILE_NEW_PASSWORD_HINT))
    password.bind("<FocusOut>", lambda event: entry_focus_out(password, PROFILE_NEW_PASSWORD_HINT))
    password.bind("<Return>", lambda event: (save_account(get_account_info(), connection), profile_frame.reload(), popup.destroy()) \
                                            if entrys_filled() else None)
    user_id = profile_frame.user[0]
    key = profile_frame.user[2]
    get_account_info = lambda: [plataform.get(),
                                encrypt_data(login.get(), key),
                                encrypt_data(password.get(), key),
                                "LOGOOO",
                                user_id]

    entrys_filled = lambda: False if plataform.get() in ("", PROFILE_NEW_PLATAFORM_HINT) \
                            or login.get() in ("", PROFILE_NEW_LOGIN_HINT) \
                            or password.get() in ("", PROFILE_NEW_PASSWORD_HINT) \
                            else True

    add = tk.Button(popup,
                    text = "add",
                    font = PROFILE_WIDGETS_FONT,
                    fg = FG,
                    bg = BG_APP,
                    command = lambda: (save_account(get_account_info(), connection), profile_frame.reload(), popup.destroy()) \
                                      if entrys_filled() else None)
    add.pack(anchor = "center")
