"""
main.py
-------
Ye program ka entry point hai. Yahan se menu chalta hai
aur user Inventory ke saath interact karta hai.
"""
from inventory import Inventory


def show_menu():
    print("\n===== INVENTORY MANAGEMENT SYSTEM =====")
    print("1. Add New Product")
    print("2. Delete Product")
    print("3. Update Quantity")
    print("4. Search Product")
    print("5. Show All Products (sorted by price)")
    print("6. Show Low Stock Items")
    print("7. Exit")


def main():
    inventory = Inventory()   # Ye khud file se purana data load kar lega

    while True:
        show_menu()
        choice = input("Choose an option (1-7): ").strip()

        try:
            if choice == "1":
                pid = int(input("Product ID: ").strip())
                name = input("Name: ").strip()
                price = float(input("Price: ").strip())
                qty = int(input("Quantity: ").strip())
                category = input("Category: ").strip()
                inventory.add_product(pid, name, price, qty, category)

            elif choice == "2":
                pid = int(input("Product ID to delete: ").strip())
                inventory.delete_product(pid)

            elif choice == "3":
                pid = int(input("Product ID: ").strip())
                amount = int(input("How much quantity? ").strip())
                action = input("increase or decrease? ").strip().lower()
                inventory.update_quantity(pid, amount, action)

            elif choice == "4":
                key = input("Search by which field? (name/category): ").strip()
                value = input("Value: ").strip()
                results = inventory.search_products(**{key: value})
                if results:
                    print(f"\n{len(results)} result(s) found:")
                    for p in results:
                        print(p)
                else:
                    print("No results found.")

            elif choice == "5":
                print("\n--- All Products (sorted by price) ---")
                for p in inventory.show_all_sorted_by_price():
                    print(p)

            elif choice == "6":
                threshold = int(input("Show items below what quantity? (default 5): ").strip() or 5)
                print(f"\n--- Low Stock Items (< {threshold}) ---")
                found = False
                for p in inventory.low_stock_items(threshold):
                    print(p)
                    found = True
                if not found:
                    print("No low stock items.")

            elif choice == "7":
                print("Exiting program. Data has been saved.")
                break

            else:
                print("Invalid option, choose between 1-7.")

        except ValueError as e:
            print(f"Input Error: {e}")
        except KeyError as e:
            print(f"Not Found Error: {e}")
        except Exception as e:
            print(f"Something went wrong: {e}")


if __name__ == "__main__":
    main()