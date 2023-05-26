import tkinter as tk
from tkinter import filedialog
from src.utils import *
from src.settings import *
from src.profileframe.utils.logohandler import *


def add_account(profile_frame: tk.Frame, window: tk.Tk, connection) -> None:
    """Creates a popup for the user to add a new account
    
    Parameters:
    profile_frame(tk.Frame): Master frame, used for calling functions
    window(tk.Tk): Window of the app
    connection(sqlite3.Connection): Connection to the database
    """
    popup = tk.Toplevel(bg = BG_APP)

    popup.title("Add Account")
    popup.iconbitmap("assets/Fort.ico")
    popup.resizable(False, False)

    widgets_holder = tk.Frame(popup,
                              bg = BG_APP)
    widgets_holder.pack(anchor = "center",
                        fill = "both",
                        expand = False)

    entrys_holder = tk.Frame(widgets_holder,
                             bg = BG_APP)
    entrys_holder.pack(anchor = "center")

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
                     relief = "solid",
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
                        width = 20,
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

    bar_frame, bar = create_strength_bar(password, entrys_holder, True)
    bar_frame.grid(row = 3,
                   column = 1,
                   sticky = "nsew")

    def update_bar(bar):
        bar["value"] = 100

    generate_image = treat_image_file("assets/GenPassword.png", (20, 20))

    generate = tk.Button(entrys_holder,
                         image = generate_image,
                         bg = BG_APP,
                         relief = "flat",
                         command = lambda entry = password, bar = bar: (generate_password(entry), update_bar(bar)))
    generate.image = generate_image
    generate.grid(row = 2,
                  column = 1,
                  sticky = "nse")

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

    add_image = treat_image_file("assets/Plus_Icon.png", (30, 30))

    add = tk.Button(widgets_holder,
                    image = add_image,
                    bg = BUTTONS_BG,
                    command = lambda: (save_account(get_account_info(), connection), profile_frame.reload(), popup.destroy()) \
                                      if entrys_filled() else None)
    add.image = add_image
    add.pack(anchor = "center",
             pady = 5)

    popup_position(popup, window)


def popup_position(popup: tk.Toplevel, window: tk.Tk):
    """Calculates the position of the main window to place the popup int the middle of it"""
    main_x = window.winfo_x()
    main_y = window.winfo_y()
    main_width = window.winfo_width()
    main_height = window.winfo_height()

    popup.update_idletasks()

    toplevel_width = popup.winfo_width()
    toplevel_height = popup.winfo_height()

    toplevel_x = main_x + (main_width - toplevel_width) // 2
    toplevel_y = main_y + (main_height - toplevel_height) // 2

    popup.geometry(f"+{toplevel_x}+{toplevel_y}")