"""
inventory.py
------------
Yahan "Inventory" class hai - ye poora register hai jo
saare Products ko manage karta hai: add, delete, search,
low-stock check, save, load.
"""
import json
import os
from product import Product
from decorators import log_action


class Inventory:
    def __init__(self, filename="inventory_data.json"):
        self.filename = filename
        self.products = {}   # Data structure: dictionary { product_id: Product object }
        self.load_from_file()   # Program start hote hi purana data load karo

    # ---------- ADD ----------
    @log_action
    def add_product(self, product_id, name, price, quantity, category):
        """Naya product inventory mein add karna"""
        if product_id in self.products:
            raise ValueError(f"ID {product_id} already exists, use a different ID")
        if price < 0 or quantity < 0:
            raise ValueError("Price or Quantity cannot be negative")

        new_product = Product(product_id, name, price, quantity, category)
        self.products[product_id] = new_product
        self.save_to_file()
        print(f"'{name}' added successfully.")

    # ---------- DELETE ----------
    @log_action
    def delete_product(self, product_id):
        """Product ko hamesha ke liye hata dena"""
        if product_id not in self.products:
            raise KeyError(f"ID {product_id} does not exist")
        removed = self.products.pop(product_id)
        self.save_to_file()
        print(f"'{removed.name}' deleted successfully.")

    # ---------- UPDATE QUANTITY ----------
    @log_action
    def update_quantity(self, product_id, amount, action="increase"):
        """Quantity badhana ya kam karna"""
        if product_id not in self.products:
            raise KeyError(f"ID {product_id} does not exist")

        product = self.products[product_id]
        if action == "increase":
            product.increase_quantity(amount)
        elif action == "decrease":
            product.decrease_quantity(amount)
        else:
            raise ValueError("Action must be 'increase' or 'decrease'")

        self.save_to_file()
        print(f"'{product.name}' quantity updated. Now: {product.quantity}")

    # ---------- SEARCH (args/kwargs use ho rahe hain - flexible search) ----------
    def search_products(self, **filters):
        """
        Flexible search - kisi bhi combination se search kar sakte ho:
        search_products(name="phone")
        search_products(category="Electronics")
        search_products(name="phone", category="Electronics")
        """
        results = []
        for product in self.products.values():
            match = True
            for key, value in filters.items():
                product_value = getattr(product, key, None)
                if product_value is None:
                    match = False
                    break
                # Text ke liye case-insensitive partial match
                if isinstance(product_value, str):
                    if value.lower() not in product_value.lower():
                        match = False
                        break
                else:
                    if product_value != value:
                        match = False
                        break
            if match:
                results.append(product)
        return results

    # ---------- SHOW ALL (Generator use ho raha hai) ----------
    def get_all_products(self):
        """
        Generator - ek time pe ek product yield karta hai,
        pura data ek saath memory mein load nahi hota.
        """
        for product in self.products.values():
            yield product

    def show_all_sorted_by_price(self):
        """Lambda use ho raha hai - price ke hisaab se sort karna"""
        sorted_products = sorted(self.products.values(), key=lambda p: p.price)
        return sorted_products

    # ---------- LOW STOCK CHECK (Generator) ----------
    def low_stock_items(self, threshold=5):
        """Generator - sirf kam-stock items ek-ek karke deta hai"""
        for product in self.products.values():
            if product.quantity < threshold:
                yield product

    # ---------- FILE HANDLING ----------
    def save_to_file(self):
        """Saara data JSON file mein save karna"""
        try:
            data = [p.to_dict() for p in self.products.values()]
            with open(self.filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving file: {e}")

    def load_from_file(self):
        """JSON file se purana data load karna, agar file exist karti hai"""
        if not os.path.exists(self.filename):
            return   # Pehli baar chal raha hai, koi purana data nahi

        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    product = Product.from_dict(item)
                    self.products[product.product_id] = product
        except (IOError, json.JSONDecodeError) as e:
            print(f"Error loading file: {e}")