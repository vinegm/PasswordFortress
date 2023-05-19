"""
Password manager
 The project focus on making a desktop app that stores the users accounts safely in a friendly and simple way
"""

import tkinter as tk
from src.utils import *
from src.loginframe import *
from src.registerframe import *
from src.profileframe import *


class PasswordFortress(tk.Tk):
    """Main class of the app, starts the database and frames"""
    def __init__(self):
        tk.Tk.__init__(self)

        self.title("PasswordFortress")
        self.eval("tk::PlaceWindow . center")
        self.iconbitmap("assets/Key.ico")

        connection = connect_database()
        
        frames_holder = tk.Frame(self)
        frames_holder.pack(anchor = "center",
                           fill = "both",
                           expand = "True")

        frames_holder.columnconfigure(0, weight = 1)
        frames_holder.rowconfigure(0, weight = 1)

        self.frames = {}
        self.initialize_frames(connection, frames_holder, ProfileFrame, RegisterFrame, LoginFrame)

        START_FRAME = "LoginFrame"
        self.change_frame(START_FRAME)

        self.mainloop()

    def initialize_frames(self, connection: sqlite3.Connection, frames_holder: tk.Frame, *frames: tk.Frame):
        """Initializes some of the frames from the app
        
        Parameters:
        connection(sqlite.Connection): Connection to the database
        frames_holder(tk.Frame): Frame where the other frames will be in
        frames(tk.Frame): Class of the frame to initialize
        """
        for f in frames:
            frame = f(connection, frames_holder, self)
            frame.grid(row = 0,
                       column = 0,
                       sticky = "nsew")
            self.frames[f.__name__] = frame

    def change_frame(self, nextFrame: str):
        """Changes between existing frames

        Parameters:
        nextFrame(str): Frame that will be raised 
        """
        frame = self.frames[nextFrame]
        frame.tkraise()
