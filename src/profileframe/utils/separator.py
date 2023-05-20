import tkinter as tk
from src.settings import *


def create_separator(master: tk.Frame) -> tk.Canvas:
    """Creates a separator, a horizontal line from one side of the window to the other
    
    Parameters:
    master(tk.frame): Where the separator will be placed

    Returns:
    separator(tk.Canvas): The created separator, only needing to place it
    """
    separator = tk.Canvas(master,
                          bg = BG_APP,
                          height = 5,
                          highlightthickness = 0)
    separator.create_line(0, 0, separator.winfo_width(), 0, fill = FG, width = 10, tag = "line")

    separator.bind("<Configure>", lambda event: separator_handler(separator))

    return separator

def separator_handler(separator: tk.Canvas):
    """Handles the size of the separator line"""
    separator.delete("line")
    separator.create_line(0, 0, separator.winfo_width(), 0, fill = FG, width = 10, tag = "line")
