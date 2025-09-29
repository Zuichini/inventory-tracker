import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from src.db import add_item, get_items

def start_app():
    """Launch the Tkinter UI for the inventory tracker."""
    root = tk.Tk()
    root.title("Inventory Tracker")
    root.geometry("600x400")

    # --- Input Frame ---
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(fill="x")

    tk.Label(frame, text="Item Name:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_name = tk.Entry(frame)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_quantity = tk.Entry(frame)
    entry_quantity.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(frame, text="Date Purchased:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_purchased = DateEntry(frame, date_pattern="yyyy-mm-dd")
    entry_purchased.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(frame, text="Expiration Date:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_expiration = DateEntry(frame, date_pattern="yyyy-mm-dd")
    entry_expiration.grid(row=3, column=1, padx=5, pady=5)

    def add_item_action():
        name = entry_name.get().strip()
        quantity = entry_quantity.get().strip()
        purchased = entry_purchased.get_date()
        expiration = entry_expiration.get_date()

        if not name or not quantity:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number")
            return

        add_item(name, quantity, purchased, expiration)
        messagebox.showinfo("Success", "Item added successfully!")
        refresh_items()

    tk.Button(frame, text="Add Item", command=add_item_action).grid(row=4, column=0, columnspan=2, pady=10)

    # --- Table for items ---
    tree = ttk.Treeview(root, columns=("id", "name", "quantity", "purchased", "expiration"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("name", text="Item Name")
    tree.heading("quantity", text="Quantity")
    tree.heading("purchased", text="Date Purchased")
    tree.heading("expiration", text="Expiration Date")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def refresh_items():
        for row in tree.get_children():
            tree.delete(row)
        items = get_items()
        for item in items:
            tree.insert("", "end", values=item)

    refresh_items()

    root.mainloop()