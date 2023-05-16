import tkinter as tk
from src.settings import *
from src.utils import *
from src.profileframe import *

class LoginFrame(tk.Frame):
    """Frame responsable for login a user in the app

    Attributes:
    Connection(sqlite3.Connection): Database of the app
    master(tk.frame): Frame where this frame will be loaded
    window(tk.Tk): Window of the app
    """
    def __init__(self, connection: sqlite3.Connection, master: tk.Frame, profile_frame: ProfileFrame, window: tk.Tk):
        tk.Frame.__init__(self, master, bg = BG_APP)

        # Header label
        header = tk.Label(self,
                          text = "Welcome to PasswordFortress!",
                          font = ("Arial", 12, "bold"),
                          fg = FG,
                          bg = BG_APP)
        header.pack(anchor = "center",
                    pady = 10)

        username = tk.Entry(self,
                            font = ("Arial", 12),
                            fg = FG,
                            bg = BG_APP)
        username.pack(anchor = "center",
                      pady = 5)

        password = tk.Entry(self,
                            font = ("Arial", 12),
                            fg = FG,
                            bg = BG_APP)
        password.pack(anchor = "center",
                      pady = 5)
        
        login = tk.Button(self,
                          text = "Login",
                          font = ("Arial", 12),
                          fg = FG,
                          bg = BG_APP)
        login.pack(anchor = "center",
                   pady = 10)

    def _loginUser (self, window, connection):
        """Checks if username and password match a user and logs said user

        Parameters:
        master: Frame that holds the loaded frames
        window: Window of the app
        connection: Main class of the app
        """
        hashed_data = hash_info()
        userInfo = user_exists(hashed_data)

        if userInfo == False:
            self.header.config(text = "Username/Password Incorrect!")
            return
        
        userPassword = userInfo[3]
        if hash_info(self.passwordEntry.get()) != userPassword:
            self.header.config(text = "Username/Password Incorrect!")
            return
        
        self._changeAndClearFrame("ProfileFrame", window)

    def _changeAndClearFrame(self, nextFrame, window):
        """Changes the raised frame and clear the widgets in this one

        Parameters:
        nextFrame: frame that will be raised
        """
        for selectEntry in ():
            selectEntry.delete(0, tk.END)
        self.header.config(text = "Welcome to a Password Manager!")
        window.change_frame(nextFrame)
