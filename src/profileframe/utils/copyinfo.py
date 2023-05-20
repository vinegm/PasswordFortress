import tkinter as tk
from src.settings import *


def create_copy_button(entry: tk.Entry, button_image: tk.PhotoImage, master: tk.Frame, window: tk.Tk) -> None:
    """Creates a button that copys the text of a given entry
    
    Parameters:
    entry(tk.Entry): The entry that the text will be copied from
    button_image(tk.PhotoImage): Image in the button
    master(tk.Frame): where this button will be placed
    window(tk.Tk): Window of the app
    """
    copy = tk.Button(master,
                     image = button_image,
                     bg = BG_APP,
                     relief = "flat",
                     command = lambda: copy_entry_text(entry, window))
    copy.image = button_image

    return copy


def copy_entry_text(entry: tk.Entry, window: tk.Tk) -> None:
    """Copys the text of a entry to the clipboard
    
    Parameters:
    entry(tk.Entry): The entry that the text will be copied from
    window(tk.Tk): Window of the app
    """
    text = entry.get()

    window.clipboard_clear()
    window.clipboard_append(text)

    return
