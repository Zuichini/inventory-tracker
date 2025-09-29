import sqlite3
import os

DB_PATH = os.path.join("data", "inventory.db")

def init_db():
    """Initialize the database and create items table if it doesn’t exist."""
    os.makedirs("data", exist_ok=True)  # ensure /data folder exists
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            date_purchased DATE NOT NULL,
            expiration_date DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_item(name, quantity, date_purchased, expiration_date):
    """Insert a new item into the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO items (name, quantity, date_purchased, expiration_date)
        VALUES (?, ?, ?, ?)
    ''', (name, quantity, date_purchased, expiration_date))
    conn.commit()
    conn.close()

def get_items():
    """Fetch all items from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM items')
    rows = c.fetchall()
    conn.close()
    return rows