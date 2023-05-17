import tkinter as tk
from src.loginframe.utils.clearframe import *


def change_frame(widgets: dict,next_frame: tk.Frame, window: tk.Tk):
    """Changes the raised frame and clear the widgets in the previous one

    Parameters:
    widgets(dict): Widgets of the frame, used for clearing the frame
    next_frame(tk.Frame): frame that will be raised
    window(tk.Tk)
    """

    clearframe(widgets)
    
    window.change_frame(next_frame)
