import tkinter as tk
from tkinter import ttk, messagebox
from src.db import add_item, get_items, delete_item, update_item
from datetime import datetime

# Refreshing the item list in the UI
def refresh_items(tree):
    tree.delete(*tree.get_children())
    items = get_items()  # (id, name, quantity, expiry_date)
    for item in items:
        item_id, name, quantity, expiry_date = item

        # Calculate days left
        if expiry_date:
            try:
                expiry = datetime.strptime(expiry_date, "%Y-%m-%d").date()
                days_left = (expiry - datetime.today().date()).days
                expiry_display = f"{days_left} days" if days_left >= 0 else "Expired"
            except ValueError:
                expiry_display = "Invalid date"
        else:
            expiry_display = "N/A"

        tree.insert("", "end", iid=item_id, values=(name, quantity, expiry_display))

# Adding new items in the inventory tracker
def open_add_popup(tree):
    popup = tk.Toplevel()
    popup.title("Add New Item")
    popup.geometry("390x220")   # fixed size window
    popup.resizable(False, False)

    # Labels and entries
    tk.Label(popup, text="Name:").grid(row=0, column=0, padx=10, pady=8, sticky="e")
    name_entry = tk.Entry(popup, width=25)
    name_entry.grid(row=0, column=1, padx=10, pady=8)

    tk.Label(popup, text="Quantity:").grid(row=1, column=0, padx=10, pady=8, sticky="e")
    quantity_entry = tk.Entry(popup, width=25)
    quantity_entry.grid(row=1, column=1, padx=10, pady=8)

    tk.Label(popup, text="Date Purchased (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=8, sticky="e")
    purchase_entry = tk.Entry(popup, width=25)
    purchase_entry.grid(row=2, column=1, padx=10, pady=8)

    tk.Label(popup, text="Expiry Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=8, sticky="e")
    expiry_entry = tk.Entry(popup, width=25)
    expiry_entry.grid(row=3, column=1, padx=10, pady=8)

    def save_item():
        name = name_entry.get().strip()
        quantity = quantity_entry.get().strip()
        purchase_date = purchase_entry.get().strip()
        expiry_date = expiry_entry.get().strip()

        # Basic validation
        if not name or not quantity:
            messagebox.showerror("Error", "Name and Quantity are required!")
            return
        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number.")
            return
        try:
            datetime.strptime(purchase_date, "%Y-%m-%d")
            datetime.strptime(expiry_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Dates must be in YYYY-MM-DD format.")
            return

        try:
            add_item(name, quantity, purchase_date, expiry_date)
            refresh_items(tree)
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Buttons
    tk.Button(popup, text="Save", command=save_item, width=12).grid(row=4, column=0, padx=10, pady=15)
    tk.Button(popup, text="Cancel", command=popup.destroy, width=12).grid(row=4, column=1, padx=10, pady=15)

    # Autofocus name field
    name_entry.focus()


# Editing existing items in the inventory tracker
def open_edit_popup(tree, item_id, name, quantity, expiry_date):
    popup = tk.Toplevel()
    popup.title("Edit Item")
    popup.resizable(False, False)

    # Labels and entries
    tk.Label(popup, text="Name").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(popup)
    name_entry.insert(0, name)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(popup, text="Quantity").grid(row=1, column=0, padx=5, pady=5)
    quantity_entry = tk.Entry(popup)
    quantity_entry.insert(0, quantity)
    quantity_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(popup, text="Expiry Date (YYYY-MM-DD)").grid(row=2, column=0, padx=5, pady=5)
    expiry_entry = tk.Entry(popup)
    expiry_entry.insert(0, expiry_date if expiry_date else "")
    expiry_entry.grid(row=2, column=1, padx=5, pady=5)

    def save_changes():
        new_name = name_entry.get()
        new_quantity = quantity_entry.get()
        new_expiry = expiry_entry.get()

        if not new_name or not new_quantity:
            messagebox.showerror("Error", "Name and Quantity are required!")
            return

        try:
            update_item(item_id, new_name, int(new_quantity), new_expiry)
            refresh_items(tree)
            popup.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(popup, text="Save Changes", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)

# Deleting items in the inventory tracker
def delete_selected_item(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select an item to delete.")
        return

    item_id = selected[0]  # Treeview iid = item_id
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?")
    if confirm:
        try:
            delete_item(item_id)
            tree.delete(item_id)  # remove from UI
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Editing selected item
def edit_selected_item(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select an item to edit.")
        return

    item_id = selected[0]
    values = tree.item(item_id, "values")
    if values:
        name, quantity, days_left = values
        # Fetch expiry date from DB
        items = get_items()
        expiry_date = None
        for i in items:
            if str(i[0]) == str(item_id):
                expiry_date = i[3]
                break
        open_edit_popup(tree, item_id, name, quantity, expiry_date)

# Handling double-click to edit items
def on_item_double_click(event, tree):
    edit_selected_item(tree)


# Starting the inventory tracker application
def start_app():
    root = tk.Tk()
    root.title("Inventory Tracker")

    # Treeview
    columns = ("Name", "Quantity", "Days Left")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Key bindings
    tree.bind("<Delete>", lambda event: delete_selected_item(tree))
    tree.bind("<Double-1>", lambda event: on_item_double_click(event, tree))

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    add_button = tk.Button(button_frame, text="Add Item", command=lambda: open_add_popup(tree))
    add_button.grid(row=0, column=0, padx=5)

    delete_button = tk.Button(button_frame, text="Delete Item", command=lambda: delete_selected_item(tree))
    delete_button.grid(row=0, column=1, padx=5)

    edit_button = tk.Button(button_frame, text="Edit Item", command=lambda: edit_selected_item(tree))
    edit_button.grid(row=0, column=2, padx=5)

    refresh_items(tree)
    root.mainloop()