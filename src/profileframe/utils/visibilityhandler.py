import tkinter as tk


def visibility_toggler(entry: tk.Entry, button: tk.Button, visibility_image: list) -> None:
    """Changes the visibility of a entry"""
    if entry.cget('show') == '':
        entry.configure(show='*')

        button.configure(image = visibility_image[1])
        button.image = visibility_image[1]

    else:
        entry.configure(show='')

        button.configure(image = visibility_image[0])
        button.image = visibility_image[0]

    return
