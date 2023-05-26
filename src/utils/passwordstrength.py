import tkinter as tk
import random as rd
import string
import re
from tkinter import ttk
from src.settings import *


def strength_checker(entry: tk.Entry, bar: ttk.Progressbar):
    """Checks the password to verify if it has a length of 12,
    lower and upper case character, a digit and a special character
    """
    patterns = [
        r".{12,}",
        r"[a-z]",
        r"[A-Z]",
        r"\d",
        r"[\W_]",
    ]

    password = entry.get()

    strength = 0
    for pattern in patterns:
        if re.search(pattern, password):
            strength += 1

    bar["value"] = strength * 20


def create_strength_bar(entry: tk.Entry, master: tk.Tk, return_bar: bool = False) -> tk.Frame:
    """Creates a frame with a bar to check the strength of a entry
    
    Parameters:
    entry(tk.Entry): The entry that will be checked
    master(tk.Frame): Where the bar will be placed

    Returns:
    widgets_holder(tk.Frame): A frame containing the progress bar
    """
    widgets_holder = tk.Frame(master,
                              bg = BG_APP)

    label = tk.Label(widgets_holder,
                     text = REGISTER_STRENGTH_TEXT,
                     font = REGISTER_STRENGTH_FONT,
                     fg = FG,
                     bg = BG_APP)
    label.pack(side = "left")

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Custom.Horizontal.TProgressbar",
                    thickness = 10,
                    troughcolor = BAR_BG,
                    background = BAR_COLOR,
                    troughrelief = "flat"
                    )

    bar = ttk.Progressbar(widgets_holder,
                          style = "Custom.Horizontal.TProgressbar",
                          mode = "determinate")
    bar.pack(side = "left",
             fill = "x",
             expand = True)

    entry.bind("<KeyRelease>", lambda event: strength_checker(entry, bar))

    if return_bar:
        return widgets_holder, bar

    return widgets_holder


def generate_password(password_entry: tk.Entry) -> None:
    """Generates a secure password with 12 to 16 characters"""
    length = rd.randint(8, 12)
    password = []

    password.append(rd.choice(string.ascii_uppercase))
    password.append(rd.choice(string.ascii_lowercase))
    password.append(rd.choice(string.digits))
    password.append(rd.choice(string.punctuation))
    
    for _ in range(length):
        password.append(rd.choice(string.ascii_letters + string.digits + string.punctuation))
    
    rd.shuffle(password)

    password = "".join(password)

    password_entry.delete(0, tk.END)
    password_entry.config(fg = FG)
    password_entry.insert(0, password)

    return
