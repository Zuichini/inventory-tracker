from src.db import add_item_to_db, update_item_in_db, delete_item_from_db, fetch_all_items

def add_item(name, quantity, date_purchased=None, expiry_date=None):
    add_item_to_db(name, quantity, date_purchased, expiry_date)

def edit_item(name, new_quantity, new_purchase_date=None, new_expiry_date=None):
    update_item_in_db(name, new_quantity, new_purchase_date, new_expiry_date)

def delete_item(name):
    delete_item_from_db(name)

def get_all_items():
    return fetch_all_items()
