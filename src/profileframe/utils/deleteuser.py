import tkinter as tk
from tkinter import messagebox
from src.utils import *
from src.settings import *

def delete_current_user(profile_frame: tk.Frame, user_info: list, window: tk.Tk, connection) -> None:
    """A popup asking to confirm the password to delete the user"""
    popup = tk.Toplevel(bg = BG_APP)

    popup.title("Delete User")
    popup.iconbitmap("assets/Fort.ico")
    popup.resizable(False, False)

    widgets_holder = tk.Frame(popup,
                              bg = BG_APP)
    widgets_holder.pack(anchor = "center",
                        fill = "both",
                        expand = False)

    text = tk.Label(widgets_holder,
                    text = "Type your password to delete your user:",
                    font = PROFILE_WIDGETS_FONT,
                    fg = FG,
                    bg = BG_APP)
    text.pack(anchor = "nw",
              padx = 10,
              pady = 5)

    password = tk.Entry(widgets_holder,
                        font = PROFILE_WIDGETS_FONT,
                        fg = FG,
                        bg = BG_APP)
    password.pack(anchor = "nw",
                  fill = "x",
                  padx = 10,
                  pady = 5)
    password.bind("<Return>", lambda event: check_password(profile_frame, user_info, password.get(), window, connection))

    buttons_holder = tk.Frame(popup,
                              bg = BG_APP)
    buttons_holder.pack(anchor = "center",
                        expand = False,
                        pady = 15)

    confirm = tk.Button(buttons_holder,
                        text = "Confirm",
                        font = PROFILE_WIDGETS_FONT,
                        fg = FG,
                        bg = BUTTONS_BG,
                        command = lambda: check_password(profile_frame, user_info, password.get(), window, connection))
    confirm.grid(row = 0,
                 column = 0,
                 padx = 10)
    
    Cancel = tk.Button(buttons_holder,
                       text = "Cancel",
                       font = PROFILE_WIDGETS_FONT,
                       fg = FG,
                       bg = BUTTONS_BG,
                       command = popup.destroy)
    Cancel.grid(row = 0,
                column = 1,
                padx = 10)

    popup_position(popup, window)

    return


def check_password(profile_frame: tk.Frame, user_info: list, typed_password: str, window: tk.Tk, connection) -> None:
    """Checks if the typed password is correct and asks for confirmation"""
    if user_info[3] == hash_wsalt(typed_password, user_info[2]):
        if messagebox.askokcancel("Confirmation", "Are you sure?"):
            delete_user(user_info[0], connection)
            profile_frame.logoff(window)
        
    else:
        messagebox.showwarning("Opss", "The password isn't correct!")

    return
