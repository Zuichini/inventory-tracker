import tkinter as tk
from datetime import datetime

def auto_resize_and_center(window):
    """Automatically adjusts window size and centers it on the screen."""
    window.update_idletasks()
    width = window.winfo_reqwidth()
    height = window.winfo_reqheight()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    window.geometry(f"+{x}+{y}")
    window.minsize(width, height)

def format_date_display(date_str):
    """Formats a stored date string into a readable display format."""
    if not date_str:
        return "-"
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%b %d, %Y")
    except ValueError:
        return date_str

def calculate_days_left(expiry_date):
    """Returns number of days left until expiry, or '-' if none."""
    if not expiry_date:
        return "-"
    try:
        expiry = expiry_date if isinstance(expiry_date, datetime) else datetime.strptime(expiry_date, "%Y-%m-%d")
        delta = (expiry - datetime.now()).days
        return delta if delta >= 0 else "Expired"
    except Exception:
        return "-"
