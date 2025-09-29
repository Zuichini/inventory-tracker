from src.ui import start_app
from src.db import init_db

if __name__ == "__main__":
    # Initialize database
    init_db()

    # Start the app
    start_app()
