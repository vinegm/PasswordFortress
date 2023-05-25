import tkinter as tk
import re
from tkinter import ttk
from src.settings import *


def strength_checker(entry, bar):
    """Checks the password to verify if it has a length of 12,
    lower and upper case character, a digit and a special character
    """
    patterns = [
        r'.{12,}',
        r'[a-z]',
        r'[A-Z]',
        r'\d',
        r'[@#$%^&+=!?><]',
    ]

    password = entry.get()

    strength = 0
    for pattern in patterns:
        if re.search(pattern, password):
            strength += 1

    bar["value"] = strength * 20


def create_strength_bar(entry, master) -> tk.Frame:
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
                     bg = BG_APP)
    label.pack(side = "left")

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Custom.Horizontal.TProgressbar",
                    thickness = 10,
                    troughcolor = "gray",
                    troughrelief = "flat",
                    background = "green"
                    )

    bar = ttk.Progressbar(widgets_holder,
                          style = "Custom.Horizontal.TProgressbar",
                          mode = "determinate")
    bar.pack(side = "left",
             fill = "x",
             expand = True)

    entry.bind("<KeyRelease>", lambda event: strength_checker(entry, bar))

    return widgets_holder
