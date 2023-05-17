import tkinter as tk
from src.settings import *

def clearframe(widgets: dict):
    """Clears the widgets from the login frame
    
    Parameter:
    widgets(dict): Dict with the widgets to be cleared, keys representing the text they should contain
    """
    for widget_text, widget in widgets.items():
        if isinstance(widget, tk.Label):
            widget.configure(text = widget_text)
        
        elif isinstance(widget, tk.Entry):
            widget.delete(0, tk.END)
            widget.config(fg = HINT_FG)
            widget.insert(0, widget_text)
