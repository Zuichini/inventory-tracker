import sqlite3
import os
from datetime import datetime

# --- Database Path ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
DB_PATH = os.path.join(DATA_DIR, "inventory.db")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    """Initialize the database if it doesn't exist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            quantity INTEGER,
            expiry_date TEXT,
            tracking_type TEXT NOT NULL DEFAULT 'quantity',
        )
    """)
    conn.commit()
    conn.close()

def add_item_to_db(name, quantity, date_purchased=None, expiry_date=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO items (name, quantity, date_purchased, expiry_date)
        VALUES (?, ?, ?, ?)
    """, (name, quantity, _format_date(date_purchased), _format_date(expiry_date)))
    conn.commit()
    conn.close()

def update_item_in_db(name, quantity, date_purchased=None, expiry_date=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE items
        SET quantity = ?, date_purchased = ?, expiry_date = ?
        WHERE name = ?
    """, (quantity, _format_date(date_purchased), _format_date(expiry_date), name))
    conn.commit()
    conn.close()

def delete_item_from_db(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE name = ?", (name,))
    conn.commit()
    conn.close()

def fetch_all_items():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, quantity, date_purchased, expiry_date FROM items")
    rows = cur.fetchall()
    conn.close()
    return rows

def _format_date(date_value):
    """Converts datetime.date or None to string for database storage."""
    if not date_value:
        return None
    if isinstance(date_value, str):
        return date_value
    return date_value.strftime("%Y-%m-%d")
