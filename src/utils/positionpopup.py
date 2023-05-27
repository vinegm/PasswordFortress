import tkinter as tk


def popup_position(popup: tk.Toplevel, window: tk.Tk):
    """Calculates the position of the main window to place the popup int the middle of it"""
    main_x = window.winfo_x()
    main_y = window.winfo_y()
    main_width = window.winfo_width()
    main_height = window.winfo_height()

    popup.update_idletasks()

    toplevel_width = popup.winfo_width()
    toplevel_height = popup.winfo_height()

    toplevel_x = main_x + (main_width - toplevel_width) // 2
    toplevel_y = main_y + (main_height - toplevel_height) // 2

    popup.geometry(f"+{toplevel_x}+{toplevel_y}")