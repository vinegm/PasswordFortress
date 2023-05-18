from src.utils import *
from src.settings import *


def register_user(nickname_entry: tk.Entry, username_entry: tk.Entry, password_entry: tk.Entry, confirm_password_entry: tk.Entry, widgets: dict, guide, connection):
    """Registers a user if all conditions are passed

    Parameters:
    nickname_entry(tk.Entry): Entry that holds the nickname of the user
    username_entry(tk.Entry): Entry that holds the username of the user
    password_entry(tk.Entry): Entry that holds the password of the user
    confirm_password_entry(tk.Entry): Entry that holds the confirmation from the password
    widgets(dict): Dict cointeining the widgets of the frame for clearing
    guide(tk.Label): Label to give feedback to the user
    connection(sqlite3.Connectio): database of the app
    """
    nickname, username, password, confirm_password = nickname_entry.get(), username_entry.get(), password_entry.get(), confirm_password_entry.get()

    if nickname == REGISTER_NICKNAME_HINT or username == REGISTER_USERNAME_HINT or password == REGISTER_PASSWORD_HINT:
        guide.configure(text = "Fill All The Boxes!",
                        fg = REGISTER_ERROR_FG)
        nickname_entry.focus()
        return

    if password != confirm_password:
        guide.configure(text = "Passwords don't match!",
                        fg = REGISTER_ERROR_FG)
        password_entry.focus()
        return

    if user_exists(username, connection) != False:
        guide.configure(text = "Username Unavailable!",
                        fg = REGISTER_ERROR_FG)
        username_entry.focus()
        return
    
    clear_frame(widgets)

    guide.configure(text = "Account Registered!",
                    fg = REGISTER_SUCCESS_FG)

    hashed_password, salt = hash_info(password)
    register_new_user(nickname, username, salt, hashed_password, connection)
