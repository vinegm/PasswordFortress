import tkinter as tk
from src.settings import *


def create_separator(master: tk.Frame):
    separator = tk.Canvas(master,
                          bg = BG_APP,
                          height = 5,
                          highlightthickness = 0)
    separator.pack(anchor = "center",
                   fill = "x")
    separator.create_line(0, 0, separator.winfo_width(), 0, fill = FG, width = 10, tag = "line")

    separator.bind("<Configure>", lambda event: separator_handler(separator))


def separator_handler(separator: tk.Canvas):
    separator.delete("line")
    separator.create_line(0, 0, separator.winfo_width(), 0, fill = FG, width = 10, tag = "line")
