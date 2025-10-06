from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QDialog, QLabel, QLineEdit, QDateEdit, QMessageBox
)
from PySide6.QtCore import Qt, QDate
import sys
from datetime import datetime
from src.db import add_item, update_item, delete_item, get_items, get_item_by_id
from src.utils import parse_date, days_until


# --- Utility to center window ---
def center_window(window, width=None, height=None):
    screen = window.screen().geometry()
    if width is None: width = window.width()
    if height is None: height = window.height()
    x = (screen.width() - width) // 2
    y = (screen.height() - height) // 2
    window.setGeometry(x, y, width, height)


# --- Main Window ---
class InventoryApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Tracker")
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Quantity", "Days Left"])
        self.table.setSelectionBehavior(self.table.SelectRows)
        self.table.setEditTriggers(self.table.NoEditTriggers)

        self.add_btn = QPushButton("Add Item")
        self.edit_btn = QPushButton("Edit Item")
        self.delete_btn = QPushButton("Delete Item")

        # Layout
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)

        layout = QVBoxLayout(self)
        layout.addLayout(btn_layout)
        layout.addWidget(self.table)

        # Signals
        self.add_btn.clicked.connect(self.open_add_popup)
        self.edit_btn.clicked.connect(self.open_edit_popup)
        self.delete_btn.clicked.connect(self.delete_item)
        self.table.cellDoubleClicked.connect(self.open_edit_popup)

        self.refresh_items()
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        center_window(self)

    # --- Refresh table ---
    def refresh_items(self):
        items = get_items()
        self.table.setRowCount(len(items))
        for row, item in enumerate(items):
            item_id, name, quantity, date_purchased, expiry_date = item
            self.table.setItem(row, 0, QTableWidgetItem(name))
            self.table.setItem(row, 1, QTableWidgetItem(str(quantity)))
            days = days_until(expiry_date)
            days_left = "N/A" if days is None else (f"{days} days" if days >= 0 else "Expired")
            self.table.setItem(row, 2, QTableWidgetItem(days_left))
            self.table.setRowHeight(row, 25)
            self.table.setRowData = item_id  # store ID for easy retrieval

    # --- Add Popup ---
    def open_add_popup(self):
        self.open_item_popup(mode="add")

    # --- Edit Popup ---
    def open_edit_popup(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "No Selection", "Please select an item to edit.")
            return
        item_id = get_items()[selected][0]
        self.open_item_popup(mode="edit", item_id=item_id)

    # --- Item Popup (Add/Edit) ---
    def open_item_popup(self, mode="add", item_id=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Item" if mode == "edit" else "Add Item")
        dialog.setModal(True)
        center_window(dialog, 350, 220)

        # Disable buttons while popup is open
        self.add_btn.setDisabled(True)
        self.edit_btn.setDisabled(True)
        self.delete_btn.setDisabled(True)

        # Re-enable buttons when popup closes
        def on_close():
            self.add_btn.setDisabled(False)
            self.edit_btn.setDisabled(False)
            self.delete_btn.setDisabled(False)
            dialog.close()

        dialog.finished.connect(on_close)

        layout = QVBoxLayout(dialog)

        # Name
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Name:"))
        name_entry = QLineEdit()
        name_layout.addWidget(name_entry)
        layout.addLayout(name_layout)

        # Quantity
        qty_layout = QHBoxLayout()
        qty_layout.addWidget(QLabel("Quantity:"))
        qty_entry = QLineEdit()
        qty_layout.addWidget(qty_entry)
        layout.addLayout(qty_layout)

        # Date Purchased
        purchase_layout = QHBoxLayout()
        purchase_layout.addWidget(QLabel("Date Purchased:"))
        purchase_entry = QDateEdit()
        purchase_entry.setDisplayFormat("yyyy-MM-dd")
        purchase_entry.setCalendarPopup(True)
        purchase_layout.addWidget(purchase_entry)
        layout.addLayout(purchase_layout)

        # Expiry Date
        expiry_layout = QHBoxLayout()
        expiry_layout.addWidget(QLabel("Expiry Date:"))
        expiry_entry = QDateEdit()
        expiry_entry.setDisplayFormat("yyyy-MM-dd")
        expiry_entry.setCalendarPopup(True)
        expiry_layout.addWidget(expiry_entry)
        layout.addLayout(expiry_layout)

        # Pre-fill if editing
        if mode == "edit" and item_id:
            item = get_item_by_id(item_id)
            _, name, quantity, date_purchased, expiry_date = item
            name_entry.setText(name)
            qty_entry.setText(str(quantity))
            if date_purchased:
                purchase_entry.setDate(parse_date(date_purchased))
            if expiry_date:
                expiry_entry.setDate(parse_date(expiry_date))

        # Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

        # Save action
        def save_action():
            name = name_entry.text().strip()
            quantity = qty_entry.text().strip()
            purchase_date = purchase_entry.date().toString("yyyy-MM-dd") if purchase_entry.date() else None
            expiry_date = expiry_entry.date().toString("yyyy-MM-dd") if expiry_entry.date() else None

            if not name or not quantity:
                QMessageBox.warning(dialog, "Error", "Name and Quantity are required!")
                return
            try:
                quantity = int(quantity)
            except ValueError:
                QMessageBox.warning(dialog, "Error", "Quantity must be a number!")
                return

            if mode == "add":
                add_item(name, quantity, purchase_date, expiry_date)
            elif mode == "edit" and item_id:
                update_item(item_id, name, quantity, purchase_date, expiry_date)

            self.refresh_items()
            on_close()

        save_btn.clicked.connect(save_action)
        cancel_btn.clicked.connect(on_close)

        dialog.exec()


    # --- Delete ---
    def delete_item(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "No Selection", "Please select an item to delete.")
            return
        item_id = get_items()[selected][0]
        confirm = QMessageBox.question(
            self, "Confirm Delete", "Are you sure you want to delete this item?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            delete_item(item_id)
            self.refresh_items()


# --- Run App ---
def start_app():
    app = QApplication(sys.argv)
    window = InventoryApp()
    window.show()
    sys.exit(app.exec())
