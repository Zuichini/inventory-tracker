import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from src.db import add_item, update_item, delete_item, get_items, get_item_by_id
from src.utils import parse_date, days_until

# --- Center main window ---
def center_window(root, width=600, height=400, x=None, y=None):
    if x is None or y is None:
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

# --- Center popup relative to parent ---
def center_popup(popup, width=400, height=250, parent=None):
    if parent:
        parent.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - height) // 2
    else:
        screen_width = popup.winfo_screenwidth()
        screen_height = popup.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
    popup.geometry(f"{width}x{height}+{x}+{y}")

# --- Refresh treeview ---
def refresh_items(tree):
    tree.delete(*tree.get_children())
    items = get_items()  # (id, name, quantity, date_purchased, expiry_date)
    for item in items:
        item_id, name, quantity, date_purchased, expiry_date = item
        days_left = days_until(expiry_date)
        expiry_display = "N/A" if days_left is None else (f"{days_left} days" if days_left >= 0 else "Expired")
        tree.insert("", "end", values=(name, quantity, expiry_display), iid=item_id)

# --- Add/Edit popup ---
def open_item_popup(tree, item=None, buttons=None, parent=None):
    # Disable main buttons
    if buttons:
        for btn in buttons:
            btn.config(state="disabled")

    popup = tk.Toplevel(parent)
    popup.title("Edit Item" if item else "Add New Item")
    popup.resizable(False, False)

    # Center the popup
    center_popup(popup, width=300, height=220, parent=parent)

    # On popup close, re-enable buttons
    def on_close():
        if buttons:
            for btn in buttons:
                btn.config(state="normal")
        popup.destroy()
    popup.protocol("WM_DELETE_WINDOW", on_close)

    # Labels & Entries
    tk.Label(popup, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    name_entry = tk.Entry(popup)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(popup, text="Quantity").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    quantity_entry = tk.Entry(popup)
    quantity_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(popup, text="Date Purchased").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    purchase_entry = DateEntry(popup, date_pattern="yyyy-mm-dd")
    purchase_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(popup, text="Expiry Date").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    expiry_entry = DateEntry(popup, date_pattern="yyyy-mm-dd")
    expiry_entry.grid(row=3, column=1, padx=5, pady=5)

    # Pre-fill if editing
    if item:
        item_id, name, quantity, date_purchased, expiry_date = item
        name_entry.insert(0, name)
        quantity_entry.insert(0, str(quantity))
        purchase_entry.set_date(parse_date(date_purchased))
        expiry_entry.set_date(parse_date(expiry_date))

    # Save function
    def save_item():
        name = name_entry.get()
        quantity = quantity_entry.get()
        purchase_date = purchase_entry.get_date().strftime("%Y-%m-%d")
        expiry_date = expiry_entry.get_date().strftime("%Y-%m-%d")

        if not name or not quantity:
            messagebox.showerror("Error", "Name and Quantity are required!")
            return

        try:
            if item:
                update_item(item[0], name, int(quantity), purchase_date, expiry_date)
            else:
                add_item(name, int(quantity), purchase_date, expiry_date)
            refresh_items(tree)
            on_close()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Centered Save/Cancel buttons
    button_frame = tk.Frame(popup)
    button_frame.grid(row=4, column=0, columnspan=2, pady=10)

    save_btn = tk.Button(button_frame, text="Save", width=12, command=save_item)
    cancel_btn = tk.Button(button_frame, text="Cancel", width=12, command=on_close)
    save_btn.pack(side="left", padx=5)
    cancel_btn.pack(side="left", padx=5)

    popup.grid_columnconfigure(0, weight=1)
    popup.grid_columnconfigure(1, weight=1)

# --- Edit selected item ---
def on_edit(tree, buttons=None, parent=None):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select an item to edit.")
        return
    item_id = selected[0]
    item = get_item_by_id(item_id)
    open_item_popup(tree, item, buttons, parent)

# --- Delete selected item ---
def on_delete(tree):
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select an item to delete.")
        return
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?")
    if confirm:
        delete_item(selected[0])
        refresh_items(tree)

# --- Main App ---
def start_app():
    root = tk.Tk()
    root.title("Inventory Tracker")
    root.resizable(False, False)
    center_window(root, width=600, height=400)

    # Buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    add_button = tk.Button(button_frame, text="Add Item", width=12,
                           command=lambda: open_item_popup(tree, buttons=[add_button, edit_button, delete_button], parent=root))
    edit_button = tk.Button(button_frame, text="Edit Item", width=12,
                            command=lambda: on_edit(tree, buttons=[add_button, edit_button, delete_button], parent=root))
    delete_button = tk.Button(button_frame, text="Delete Item", width=12,
                              command=lambda: on_delete(tree))

    add_button.pack(side="left", padx=5)
    edit_button.pack(side="left", padx=5)
    delete_button.pack(side="left", padx=5)

    # Treeview
    columns = ("Name", "Quantity", "Days Left")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Double-click row to edit
    tree.bind("<Double-1>", lambda e: on_edit(tree, buttons=[add_button, edit_button, delete_button], parent=root))

    refresh_items(tree)
    root.mainloop()