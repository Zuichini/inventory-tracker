import sqlite3
import os
from src.utils import format_date

DB_PATH = os.path.join("data", "inventory.db")

def init_db():
    """Initialize the database and create items table if it doesn’t exist."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            date_purchased DATE NOT NULL,
            expiry_date DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- CRUD operations ---
def add_item(name, quantity, date_purchased, expiry_date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO items (name, quantity, date_purchased, expiry_date)
        VALUES (?, ?, ?, ?)
    ''', (name, quantity, date_purchased, expiry_date))
    conn.commit()
    conn.close()

def get_items():
    """Fetch all items from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM items ORDER BY expiry_date ASC')
    rows = c.fetchall()
    conn.close()
    return rows

def get_item_by_id(item_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM items WHERE id=?', (item_id,))
    row = c.fetchone()
    conn.close()
    return row

def update_item(item_id, name, quantity, date_purchased, expiry_date):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE items
        SET name=?, quantity=?, date_purchased=?, expiry_date=?
        WHERE id=?
    ''', (name, quantity, date_purchased, expiry_date, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id=?', (item_id,))
    conn.commit()
    conn.close()