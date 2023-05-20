import tkinter as tk
from src.utils.encryptionhandler import *
from src.utils.databasehandler import *


def edit_account(edit_button: tk.Button, button_images: tk.PhotoImage, account_id: int, key: bytes, connection, entrys: list) -> None:
    edit_button.configure(image = button_images[0],
                          command = lambda: save_edit(edit_button, button_images, account_id, entrys, key, connection))
    edit_button.image = button_images[0]

    for entry in entrys:
        entry.configure(state = "normal",
                        relief = "groove")

    return


def save_edit(edit_button: tk.Button, button_images: tk.PhotoImage, account_id: int, entrys: list, key: bytes, connection) -> None:
    edit_button.configure(image = button_images[1],
                          command = edit_account(edit_button, button_images, account_id, key, connection, entrys))
    edit_button.image = button_images[1]
    
    account_update = [entrys[0].get()]
    
    entrys[0].configure(state = "disabled",
                        relief = "flat")

    for entry in entrys[1:]:
        input = entry.get()

        entry.configure(state = "disabled",
                        relief = "flat")

        account_update.append(encrypt_data(input, key))

    account_update.append(account_id)
    update_account(account_update, connection)

    return
