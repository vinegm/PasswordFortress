import tkinter as tk
from src.utils import *
from src.profileframe.utils import *


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
        self.header_changer = lambda: header.configure(text = self.user[1])
        
        logoff = tk.Button(header_holder,
                           text = "logoff",
                           font = PROFILE_WIDGETS_FONT,
                           fg = FG,
                           bg = BG_APP,
                           command = lambda: window.change_frame("LoginFrame"))
        logoff.configure(relief = tk.FLAT)
        logoff.grid(row = 0,
                    column = 0,
                    sticky = "w")

        create_separator(widgets_holder)

        accounts = tk.Frame(widgets_holder,
                            bg = BG_APP)
        accounts.pack(anchor = "center",
                      fill = "x")
        
        self.accounts_loader = lambda: populate_accounts(accounts, self.user[0], self.user[2], connection)
        self.accounts_holder = self.accounts_loader()

        add = tk.Button(widgets_holder,
                                text = "ADD",
                                font = PROFILE_WIDGETS_FONT,
                                fg = FG,
                                bg = BG_APP,
                                command = lambda: add_account(self, connection))
        add.pack(anchor = "center")

    def reload(self, changing_user: bool = False) -> None:
        """Reloads the header and accounts of the Profile frame
        
        Parameters:
        changing_user(bool): Only turned to true when changing the logged used
        """
        if changing_user:
            self.header_changer()
        
        if self.accounts_holder != None:
            self.accounts_holder.destroy()

        self.accounts_holder = self.accounts_loader()
        return
