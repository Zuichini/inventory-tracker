import sqlite3

# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

# Create items table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    purchase_date DATE,
    expiry_date DATE,
    status TEXT DEFAULT 'active'
)
""")

# --- Functions ---
def add_item(name, quantity, purchase_date, expiry_date):
    cursor.execute("""
    INSERT INTO items (name, quantity, purchase_date, expiry_date)
    VALUES (?, ?, ?, ?)
    """, (name, quantity, purchase_date, expiry_date))
    conn.commit()

def list_items():
    cursor.execute("SELECT * FROM items")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# --- Example usage ---
if __name__ == "__main__":
    add_item("Milk", 2, "2025-09-29", "2025-10-05")
    print("📦 Current Items in Inventory:")
    list_items()
