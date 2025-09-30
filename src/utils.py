from datetime import datetime, date

def format_date(date_obj):
    """Convert a date object to string YYYY-MM-DD."""
    if isinstance(date_obj, (datetime, date)):
        return date_obj.strftime("%Y-%m-%d")
    return str(date_obj)

def parse_date(date_str):
    """Convert YYYY-MM-DD string to a date object."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None

def days_until(expiry_date):
    """Calculate days left until expiry. Returns int or None."""
    expiry = parse_date(expiry_date)
    if expiry:
        delta = (expiry - datetime.today().date()).days
        return delta
    return None
