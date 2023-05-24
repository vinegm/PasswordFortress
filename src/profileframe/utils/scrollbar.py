import tkinter as tk
from src.settings import *


def create_scrollbar_zone(master: tk.Frame, window: tk.Tk):
    """Creates a frame with a scroll bar and returns it"""
    scrollbar = tk.Scrollbar(master)
    scrollbar.pack(side = "right",
                   fill = "y")

    canvas = tk.Canvas(master,
                       bg = BG_APP,
                       yscrollcommand = scrollbar.set)
    canvas.pack(anchor = "center",
                fill = "both",
                expand = True)

    scrollbar.config(command = canvas.yview)

    frame = tk.Frame(canvas,
                     bg = BG_APP)
    canvas.create_window((0, 0),
                         anchor = "nw",
                         window = frame,
                         tags = "frame")

    window.bind("<Configure>", lambda _: on_configure(frame, canvas))
    frame.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))

    return frame


def on_mousewheel(event: tk. Event, canvas: tk.Canvas):
    """Handles the use of the mousewheel to scroll"""
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


def on_configure(frame: tk.Frame, canvas: tk.Canvas):
    """Handles the size of the frame if the window changes size"""
    canvas.configure(scrollregion = canvas.bbox("all"))
    canvas.itemconfig("frame", width = canvas.winfo_width())

    canvas_height = canvas.winfo_height()
    frame_height = frame.winfo_reqheight()

    if frame_height > canvas_height:
        canvas.configure(scrollregion = (0, 0, frame.winfo_reqwidth(), frame_height))
        frame.bind_all("<MouseWheel>", lambda event: on_mousewheel(event, canvas))
    else:
        frame.unbind_all("<MouseWheel>")