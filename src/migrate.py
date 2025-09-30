import sqlite3
import os

DB_PATH = "inventory.db"
MIGRATIONS_PATH = "migrations"

def run_migrations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create table to track applied migrations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL UNIQUE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Get already applied migrations
    cursor.execute("SELECT filename FROM migrations")
    applied = {row[0] for row in cursor.fetchall()}

    # Run any new migrations
    for filename in sorted(os.listdir(MIGRATIONS_PATH)):
        if filename.endswith(".sql") and filename not in applied:
            print(f"Applying {filename}...")
            with open(os.path.join(MIGRATIONS_PATH, filename), "r") as f:
                sql = f.read()
                cursor.executescript(sql)
            cursor.execute("INSERT INTO migrations (filename) VALUES (?)", (filename,))
            conn.commit()

    conn.close()
    print("✅ All migrations applied.")

if __name__ == "__main__":
    run_migrations()
