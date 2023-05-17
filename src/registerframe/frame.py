import tkinter as tk
from src.utils import *
from src.settings import *


class RegisterFrame(tk.Frame):
    """Frame responsable for registering a user in the app

    Attributes:
    Connection: Database of the app
    master: Widget/window where this frame will be loaded
    controller: Main class of the app

    Methods:
    _registerUser: Registers a user if all the "if's" are passed and returns to the LoginFrame
    _return: Returns to the LoginFrame and clears all the widgets from this one
    """
    def __init__(self, connection: sqlite3.Connection, master: tk.Frame, window: tk.Tk):
        tk.Frame.__init__(self, master, bg = BG_APP)

        widgets_holder = tk.Frame(self,
                                  bg = BG_APP)
        widgets_holder.pack(expand = True)

        header = tk.Label(widgets_holder,
                          text = "Welcome to PasswordFortress!",
                          font = ("Arial", 12, "bold"),
                          fg = FG,
                          bg = BG_APP)
        header.pack(anchor = "center",
                    pady = 10)

        nickname = tk.Entry(widgets_holder,
                            font = ("Arial", 12),
                            fg = HINT_FG,
                            bg = BG_APP)
        nickname.pack(anchor = "center",
                      pady = 5)
        NICKNAME_HINT = "Enter a Nickname"
        nickname.insert(0, NICKNAME_HINT)
        nickname.bind('<FocusIn>', lambda event: entry_focus_in(nickname, NICKNAME_HINT))
        nickname.bind('<FocusOut>', lambda event: entry_focus_out(nickname, NICKNAME_HINT))

        username = tk.Entry(widgets_holder,
                            font = ("Arial", 12),
                            fg = HINT_FG,
                            bg = BG_APP)
        username.pack(anchor = "center",
                      pady = 5)
        USERNAME_HINT = "Enter a Username"
        username.insert(0, USERNAME_HINT)
        username.bind('<FocusIn>', lambda event: entry_focus_in(username, USERNAME_HINT))
        username.bind('<FocusOut>', lambda event: entry_focus_out(username, USERNAME_HINT))

        password = tk.Entry(widgets_holder,
                            font = ("Arial", 12),
                            fg = HINT_FG,
                            bg = BG_APP)
        password.pack(anchor = "center",
                      pady = 5)
        PASSWORD_HINT = "Enter a Password"
        password.insert(0, PASSWORD_HINT)
        password.bind('<FocusIn>', lambda event: entry_focus_in(password, PASSWORD_HINT))
        password.bind('<FocusOut>', lambda event: entry_focus_out(password, PASSWORD_HINT))
        
        register = tk.Button(widgets_holder,
                          text = "register",
                          font = ("Arial", 12),
                          fg = FG,
                          bg = BG_APP)
        register.pack(anchor = "center",
                   pady = 10)

        back = tk.Button(widgets_holder,
                          text = "back",
                          font = ("Arial", 12),
                          fg = FG,
                          bg = BG_APP,
                          command = lambda: window.change_frame("LoginFrame"))
        back.configure(relief = tk.FLAT)
        back.pack(anchor = "center",
                   pady = 10)

    def _registerUser(self, controller, connection):
        """Registers a user if all the "if's" are passed and returns to the LoginFrame

        Parameters:
        controller: Main class of the app
        connection: database of the app
        """
        # If a box is left empty
        if self.nicknameEntry.get() == "" or self.usernameEntry.get() == "" or self.passwordEntry.get() == "":
            self.header.config(text = "Fill All The Boxes!")
            return

        # If a username is already in use
        if user_exists(username := hash_info(self.usernameEntry.get()), connection) != False:
            self.header.config(text = "Username Unavailable!")
            return

        # If password and the password confirmation dont match
        if self.confirmPasswordEntry.get() != self.passwordEntry.get():
            self.header.config(text = "Passwords Don't Match!")
            return

        # Registers the user if everything is ok
        nickname = self.nicknameEntry.get()
        password = hash_info(self.passwordEntry.get())
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (nickname, username, password) VALUES (?, ?, ?)", (nickname, username, password))
        connection.commit()
        cursor.close()
        self._return(controller)

    def _return(self, controller):
        """Returns to the LoginFrame and clears all the widgets from this one
        
        Parameters:
        Controller: Main class of the app, used to call the function to change frame
        """
        for selectEntry in (self.nicknameEntry, self.usernameEntry, self.passwordEntry, self.confirmPasswordEntry):
            selectEntry.delete(0, tk.END)
        self.header.config(text = "Register an Account!")
        controller.change_frame("LoginFrame")
