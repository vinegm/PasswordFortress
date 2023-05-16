import tkinter as tk
from src.settings import *


def entry_focus_in(entry: tk.Entry, entry_hint: str):
    """Handles the focus in the entry for removing the hint
    
    Parameters:
    entry(tk.Entry): Entry that holdes the hint
    entry_hint(str): Text the hint shows
    """
    if entry.get() == entry_hint:
        entry.delete(0, tk.END)
        entry.config(fg = FG)


def entry_focus_out(entry: tk.Entry, entry_hint: str):
    """Handles the focus out of the entry for adding the hint if necessary
    
    Parameters:
    entry(tk.Entry): Entry that holdes the hint
    entry_hint(str): Text the hint shows
    """
    if entry.get() == "":
        entry.insert(0, entry_hint)
        entry.config(fg = HINT_FG)
