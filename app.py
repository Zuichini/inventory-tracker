# app.py
import sys
from PySide6.QtWidgets import QApplication
from src.ui import InventoryUI

def main():
    app = QApplication(sys.argv)
    window = InventoryUI()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
