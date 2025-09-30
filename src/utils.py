# Placeholder for helper functions we may need later
# Example: date formatting, expiration status checks, etc.
from datetime import datetime, date

def format_date(date_obj):
    """Convert a date object to string YYYY-MM-DD."""
    return date_obj.strftime("%Y-%m-%d")


def parse_date(date_str):
    """Convert YYYY-MM-DD string to a date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()

def safe_to_date(value):
    """Convert DB value (str or date) to a date object safely."""
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return parse_date(value)
        except ValueError:
            return None
    return None

def days_until(expiry_date):
    """Return human-readable days left until expiry."""
    expiry = safe_to_date(expiry_date)
    if not expiry:
        return "Invalid date"

    days_left = (expiry - datetime.today().date()).days
    return f"{days_left} days" if days_left >= 0 else "Expired"