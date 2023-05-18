import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
from io import BytesIO
from src.utils import *


class ProfileFrame(tk.Frame):
    """Frame responsable for displaying the user stored accounts

    Attributes:
    Connection(sqlite3.Connection): Database of the app
    master(tk.frame): Frame where this frame will be loaded
    window(tk.Tk): Window of the app
    """
    def __init__(self, connection: sqlite3.Connection, master: tk.Frame, window: tk.Tk):
        tk.Frame.__init__(self, master, bg = BG_APP)

        self.user = [None, "Placeholder", None]

        widgets_holder = tk.Frame(self,
                                  bg = BG_APP)
        widgets_holder.pack(fill = "both",
                            expand = True)

        header_holder = tk.Frame(widgets_holder,
                                 bg = BG_APP,
                                 border = 1)
        header_holder.pack(anchor = "center",
                           fill = "x")
        header_holder.columnconfigure(1, weight = 1)

        header = tk.Label(header_holder,
                          text = self.user[1],
                          font = PROFILE_HEADER_FONT,
                          fg = FG,
                          bg = BG_APP)
        header.grid(row = 0,
                    column = 0, columnspan = 3,
                    sticky = "nsew")
        
        logoff = tk.Button(header_holder,
                           text = "logoff",
                           font = PROFILE_HEADER_FONT,
                           fg = FG,
                           bg = BG_APP,
                           command = lambda: (window.change_frame("LoginFrame"), print(self.user)))
        logoff.configure(relief = tk.FLAT)
        logoff.grid(row = 0,
                    column = 0,
                    sticky = "w")
