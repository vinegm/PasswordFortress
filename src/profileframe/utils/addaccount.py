import tkinter as tk
from tkinter import filedialog
from src.utils import *
from src.settings import *
from src.profileframe.utils.logohandler import *


def add_account(profile_frame: tk.Frame, connection) -> None:
    """Creates a popup for the user to add a new account
    
    Parameters:
    profile_frame(tk.Frame): Master frame, used for calling functions
    connection(sqlite3.Connection): Connection to the database
    """
    popup = tk.Toplevel(bg = BG_APP)

    entrys_holder = tk.Frame(popup,
                             bg = BG_APP)
    entrys_holder.pack(anchor = "center",
                       fill = "x")

    def select_logo():
        """Selects a logo for the plataform"""
        nonlocal logo_image
        logo_path = filedialog.askopenfilename(filetypes = [("Image files", "*.png;*.jpg;*.jpeg")])
        if logo_path:
            logo_image = treat_image_file(logo_path)

            logo.configure(image = logo_image)
            logo.image = logo_image

    logo_image = treat_logo(None)

    logo = tk.Button(entrys_holder,
                     image = logo_image,
                     bg = BG_APP,
                     relief = "flat",
                     command = select_logo)
    logo.image = logo_image
    logo.grid(row = 0, rowspan = 3,
              column = 0,
              sticky = "nsew",
              padx = 10,
              pady = 5)
    
    logo_image = None

    plataform = tk.Entry(entrys_holder,
                         font = PROFILE_WIDGETS_FONT,
                         fg = HINT_FG,
                         bg = BG_APP)
    plataform.grid(row = 0,
                   column = 1,
                   pady = 5,
                   sticky = "nsw")
    plataform.insert(0, PROFILE_NEW_PLATAFORM_HINT)
    plataform.bind("<FocusIn>", lambda event: entry_focus_in(plataform, PROFILE_NEW_PLATAFORM_HINT))
    plataform.bind("<FocusOut>", lambda event: entry_focus_out(plataform, PROFILE_NEW_PLATAFORM_HINT))
    plataform.bind("<Return>", lambda event: login.focus())

    login = tk.Entry(entrys_holder,
                     font = PROFILE_WIDGETS_FONT,
                     fg = HINT_FG,
                     bg = BG_APP)
    login.grid(row = 1,
               column = 1,
               pady = 5,
               sticky = "nsw")
    login.insert(0, PROFILE_NEW_LOGIN_HINT)
    login.bind("<FocusIn>", lambda event: entry_focus_in(login, PROFILE_NEW_LOGIN_HINT))
    login.bind("<FocusOut>", lambda event: entry_focus_out(login, PROFILE_NEW_LOGIN_HINT))
    login.bind("<Return>", lambda event: password.focus())

    password = tk.Entry(entrys_holder,
                        font = PROFILE_WIDGETS_FONT,
                        fg = HINT_FG,
                        bg = BG_APP)
    password.grid(row = 2,
                  column = 1,
                  pady = 5,
                  sticky = "nsw")
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
                                logo_to_bytes(logo_image),
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
                    width = 5,
                    command = lambda: (save_account(get_account_info(), connection), profile_frame.reload(), popup.destroy()) \
                                      if entrys_filled() else None)
    add.pack(anchor = "center",
             pady = 5)
