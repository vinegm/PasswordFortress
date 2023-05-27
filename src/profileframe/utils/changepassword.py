import tkinter as tk
from tkinter import messagebox
from src.utils import *
from src.settings import *


def change_password(profile_frame: tk.Frame, user_info: list, window: tk.Tk, connection) -> None:
    popup = tk.Toplevel(bg = BG_APP)

    popup.title("Change Password")
    popup.iconbitmap("assets/Fort.ico")
    popup.resizable(False, False)

    widgets_holder = tk.Frame(popup,
                              bg = BG_APP)
    widgets_holder.pack(anchor = "center",
                        fill = "both",
                        expand = False)

    text = tk.Label(widgets_holder,
                    text = CHANGING_HEADER_PASSWORD,
                    font = PROFILE_WIDGETS_FONT,
                    fg = FG,
                    bg = BG_APP)
    text.pack(anchor = "nw",
              padx = 10,
              pady = 5)

    guide = tk.Label(widgets_holder,
                     text = CHANGING_GUIDE_TEXT,
                     font = PROFILE_WIDGETS_FONT,
                     fg = FG,
                     bg = BG_APP)
    guide.pack(anchor = "nw",
               padx = 10,
               pady = 5)

    old_password = tk.Entry(widgets_holder,
                            font = PROFILE_WIDGETS_FONT,
                            fg = HINT_FG,
                            bg = BG_APP)
    old_password.pack(anchor = "nw",
                      fill = "x",
                      padx = 10,
                      pady = 10)
    old_password.insert(0, OLD_PASSWORD_HINT)
    old_password.bind("<FocusIn>", lambda event: entry_focus_in(old_password, OLD_PASSWORD_HINT))
    old_password.bind("<FocusOut>", lambda event: entry_focus_out(old_password, OLD_PASSWORD_HINT))
    old_password.bind("<Return>", lambda event: new_password.focus())
    
    new_password = tk.Entry(widgets_holder,
                            font = PROFILE_WIDGETS_FONT,
                            fg = HINT_FG,
                            bg = BG_APP)
    new_password.pack(anchor = "nw",
                      fill = "x",
                      padx = 10)
    new_password.insert(0, NEW_PASSWORD_HINT)
    new_password.bind("<FocusIn>", lambda event: entry_focus_in(new_password, NEW_PASSWORD_HINT))
    new_password.bind("<FocusOut>", lambda event: entry_focus_out(new_password, NEW_PASSWORD_HINT))
    new_password.bind("<Return>", lambda event: confirm_password.focus())
    
    confirm_password = tk.Entry(widgets_holder,
                                font = PROFILE_WIDGETS_FONT,
                                fg = HINT_FG,
                                bg = BG_APP)
    confirm_password.pack(anchor = "nw",
                          fill = "x",
                          padx = 10,
                          pady = 5)
    confirm_password.insert(0, CONFIRM_PASSWORD_HINT)
    confirm_password.bind("<FocusIn>", lambda event: entry_focus_in(confirm_password, CONFIRM_PASSWORD_HINT))
    confirm_password.bind("<FocusOut>", lambda event: entry_focus_out(confirm_password, CONFIRM_PASSWORD_HINT))
    confirm_password.bind("<Return>", lambda event: check_passwords(old_password.get(), new_password.get(), confirm_password.get(),
                                                                    guide, popup, profile_frame, user_info, window, connection))
    
    buttons_holder = tk.Frame(popup,
                              bg = BG_APP)
    buttons_holder.pack(anchor = "center",
                        expand = False,
                        pady = 15)

    confirm = tk.Button(buttons_holder,
                        text = CONFIRM_TEXT,
                        font = PROFILE_WIDGETS_FONT,
                        fg = FG,
                        bg = BUTTONS_BG,
                        command = lambda: check_passwords(old_password.get(), new_password.get(), confirm_password.get(),
                                                          guide, popup, profile_frame, user_info, window, connection))
    confirm.grid(row = 0,
                 column = 0,
                 padx = 10)

    Cancel = tk.Button(buttons_holder,
                       text = CANCEL_TEXT,
                       font = PROFILE_WIDGETS_FONT,
                       fg = FG,
                       bg = BUTTONS_BG,
                       command = popup.destroy)
    Cancel.grid(row = 0,
                column = 1,
                padx = 10)

    popup_position(popup, window)

    return


def check_passwords(old: str, new: str, confirmation: str, guide: tk.Label, popup: tk.Toplevel, profile_frame: tk.Frame, user_info: list, window: tk.Tk, connection) -> None:
    if "" in [old, new, confirmation]:
        guide.configure(text = "Fill ALL the Boxes:",
                        fg = ON_CHANGING_ERROR)

        return
    
    if new != confirmation:
        guide.configure(text = "Confirmation does Not Match!",
                        fg = ON_CHANGING_ERROR)

        return

    if user_info[3] != hash_wsalt(old, user_info[2]):
        guide.configure(text = "Old Password Incorrect!",
                        fg = ON_CHANGING_ERROR)

        return

    else:
        guide.configure(text = "Updating Your Data!",
                        fg = ON_CHANGING_SUCESS)

        new_password, new_salt = hash_info(new)
        update_password(user_info[0], new_salt, new_password, connection)

        new_key = KDF(new, new_salt)
        old_key = user_info[4]

        user_info[2], user_info[3] = new_salt, new_password
        profile_frame.user[2], profile_frame.user[3], profile_frame.user[4] = new_salt, new_password, new_key

        update_wnew_key(user_info, old_key, new_key, connection)

        popup.destroy()

        return


def update_wnew_key(user_info: list, old_key: bytes, new_key: bytes, connection):
    accounts = get_accounts_info(user_info[0], connection)
    if not accounts:
        return

    for account in accounts:
        updated_account = []
        for i, encrypted_info in enumerate(account[1:]):
            info = decrypt_data(encrypted_info, old_key)

            updated_account.append(encrypt_data(info, new_key))

        updated_account.append(account[0])

        update_account_info(updated_account, connection)

    return