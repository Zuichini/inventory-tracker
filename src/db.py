import sqlite3
import os

DB_PATH = os.path.join("data", "inventory.db")

# Database initialization and connection
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
            expiry_date DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# CRUD operations
# Create
def add_item(name, quantity, date_purchased, expiry_date):
    """Insert a new item into the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO items (name, quantity, date_purchased, expiry_date)
        VALUES (?, ?, ?, ?)
    ''', (name, quantity, date_purchased, expiry_date))
    conn.commit()
    conn.close()

# Read
def get_items():
    """Fetch all items from the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id, name, quantity, expiry_date FROM items')
    rows = c.fetchall()
    conn.close()
    return rows

# Delete
def delete_item(item_id):
    """Delete an item from the database by ID."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

# Update
def update_item(item_id, name, quantity, expiry_date):
    """Update an item in the database."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        UPDATE items
        SET name = ?, quantity = ?, expiry_date = ?
        WHERE id = ?
    ''', (name, quantity, expiry_date, item_id))
    conn.commit()
    conn.close()
