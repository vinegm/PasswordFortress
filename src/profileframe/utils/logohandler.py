import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO


def treat_image_file(logo_path: str, size: tuple = (75, 75)) -> tk.PhotoImage:
    """Takes a file path and converts it to a tkinter photo image
    
    Parameter:
    logo_path(str): Path to the logo

    Retruns:
    logo(tk.PhotoImage): The treated logo
    """
    logo = Image.open(logo_path)
    logo = logo.resize(size)

    logo = ImageTk.PhotoImage(logo)
    return logo


def treat_logo(logo: bytes) -> tk.PhotoImage:
    """Treats the logo blob for it to be used in tkinter
    
    Parameters:
    logo(bytes): The bytes blob of the logo

    Returns:
    logo(tk.PhotoImage): The logo or a placeholder for it
    """
    # Checks if is has a logo, if it doesn't assings it a placeholder
    if logo == None:
        logo = treat_image_file("assets/Question_Mark.png")

        return logo
    
    image_buffer = BytesIO(logo)
    logo = Image.open(image_buffer)

    logo = ImageTk.PhotoImage(logo)

    return logo


def logo_to_bytes(logo: tk.PhotoImage) -> bytes:
    """Turns the logo from a tkinter photo image to a bytes blob
    
    Parameter:
    logo(tk.PhotoImage): The photo image that will be converted

    Returns:
    logo_bytes(bytes): The bytes blob of the logo
    """
    if logo == None:
        return None
    
    logo = ImageTk.getimage(logo)

    image_buffer = BytesIO()
    logo.save(image_buffer, format='PNG')

    logo_bytes = image_buffer.getvalue()

    return logo_bytes