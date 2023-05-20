import tkinter as tk
from tkinter import filedialog
from src.settings import *
from src.utils import *
from src.profileframe.utils.separator import *
from src.profileframe.utils.logohandler import *


def populate_accounts(master: tk.Frame, user_id: int, key: bytes, connection) -> tk.Frame:
    """Populates the profile frame with the users accounts

    Parameters:
    master(tk.Frame): Frame that will hold the widgets
    user_id(int): Id of the current user
    key(bytes): Cryptography key of the user
    connection(sqlite3.Connection): Connection to the database

    Returns:
    accounts_holder(tk.Frame): Frame containing all the widgets from the user accounts
    """
    if user_id == None:
        return None

    accounts = get_accounts(user_id, connection)

    accounts_holder = tk.Frame(master,
                               bg = BG_APP)
    accounts_holder.pack(anchor = "center",
                         fill = "x")

    delete_image = treat_image_file("assets/Delete.png")
    edit_image = treat_image_file("assets/Edit.png")

    for account in accounts:
        account = list(account)
        account[2] = decrypt_data(account[2], key)
        account[3] = decrypt_data(account[3], key)

        account_frame = tk.Frame(accounts_holder,
                                 bg = BG_APP)
        account_frame.pack(anchor = "center",
                           fill = "x",
                           expand = True)
        account_frame.columnconfigure(1, weight = 1)

        def change_logo():
            """change the logo for the plataform"""
            nonlocal logo_image
            logo_path = filedialog.askopenfilename(filetypes = [("Image files", "*.png;*.jpg;*.jpeg")])
            if logo_path:
                logo_image = treat_image_file(logo_path)

                logo.configure(image = logo_image)
                logo.image = logo_image

                update_logo(logo_to_bytes(logo_image), account[0], connection)

        logo_image = treat_logo(account[4])

        logo = tk.Button(account_frame,
                         image = logo_image,
                         bg = BG_APP,
                         relief = "flat",
                         command = change_logo)
        logo.image = logo_image
        logo.grid(row = 0, rowspan = 3,
                  column = 0,
                  sticky = "nsew",
                  padx = 10,
                  pady = 5)

        plataform = tk.Entry(account_frame,
                             font = PROFILE_WIDGETS_FONT,
                             justify = "left",
                             fg = FG,
                             disabledforeground = FG,
                             bg = BG_APP,
                             disabledbackground = BG_APP,
                             relief = "flat")
        plataform.insert(0, account[1])
        plataform.configure(state = "disabled")
        plataform.grid(row = 0,
                       column = 1,
                       sticky = "nsew")

        login = tk.Entry(account_frame,
                         font = PROFILE_WIDGETS_FONT,
                         justify = "left",
                         fg = FG,
                         disabledforeground = FG,
                         bg = BG_APP,
                         disabledbackground = BG_APP,
                         relief = "flat")
        login.insert(0, account[2])
        login.configure(state = "disabled")
        login.grid(row = 1,
                   column = 1,
                   sticky = "nsew")
        
        password = tk.Entry(account_frame,
                            font = PROFILE_WIDGETS_FONT,
                            justify = "left",
                            fg = FG,
                            disabledforeground = FG,
                            bg = BG_APP,
                            disabledbackground = BG_APP,
                            relief = "flat")
        password.insert(0, account[3])
        password.configure(state = "disabled")
        password.grid(row = 2,
                      column = 1,
                      sticky = "nsew")

        edit_button = tk.Button(account_frame,
                                image = edit_image,
                                bg = BG_APP,
                                relief = "flat")
        edit_button.image = edit_image
        edit_button.grid(row = 0, rowspan = 3,
                         column = 2,
                         sticky = "nsew",
                         padx = 10,
                         pady = 5)

        delete_acc = lambda frame = account_frame, account_id = account[0]: \
                     (frame.destroy(), delete_account(account_id, connection))

        delete_button = tk.Button(account_frame,
                                  image = delete_image,
                                  bg = BG_APP,
                                  relief = "flat",
                                  command = delete_acc)
        delete_button.image = delete_image
        delete_button.grid(row = 0, rowspan = 3,
                           column = 3,
                           sticky = "nsew",
                           padx = 10,
                           pady = 5)

        separator = create_separator(account_frame)
        separator.grid(column = 0, columnspan = 4,
                       sticky = "ew")

    return accounts_holder
