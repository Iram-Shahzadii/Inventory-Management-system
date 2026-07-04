"""
product.py
-----------
Yahan "Product" class hai — ye ek single item ki detail hai
(jaise register ka ek page). OOP concept yahan use ho raha hai.
"""


class Product:
    def __init__(self, product_id, name, price, quantity, category):
        # Har product ki 5 basic details (attributes)
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

    def increase_quantity(self, amount):
        """Naya maal aaye to quantity badhana"""
        if amount <= 0:
            raise ValueError("Amount to increase must be positive")
        self.quantity += amount

    def decrease_quantity(self, amount):
        """Item bike to quantity kam karna"""
        if amount <= 0:
            raise ValueError("Amount to decrease must be positive")
        if amount > self.quantity:
            raise ValueError(f"Only {self.quantity} pieces in stock, cannot decrease by this much")
        self.quantity -= amount

    def update_price(self, new_price):
        """Price update karna"""
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = new_price

    def to_dict(self):
        """Product ko dictionary mein convert karna - file mein save karne ke liye"""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category
        }

    @classmethod
    def from_dict(cls, data):
        """Dictionary se dobara Product object banana - file se load karte waqt"""
        return cls(
            data["product_id"],
            data["name"],
            data["price"],
            data["quantity"],
            data["category"]
        )

    def __str__(self):
        """Product ki detail readable tareeke se dikhana"""
        return (f"ID: {self.product_id} | {self.name} | "
                f"Price: {self.price} | Qty: {self.quantity} | "
                f"Category: {self.category}")