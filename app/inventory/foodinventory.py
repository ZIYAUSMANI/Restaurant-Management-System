from ..domain.filehandler import Createfile
from ..model.models import PathModel
from ..model.models import InventoryItemModel
from ..validation.checkvalidation import Validationcheck
from ..logs.logger import get_logger
from datetime import datetime

class FoodInventorymanagment:
    """
    Inventorymanagment handles complete food inventory operations.
    It allows adding, updating, deleting, and searching food items.
    The system automatically removes expired items before operations.
    Inventory data is stored in files and validated using Validationcheck.
    Logging is used to track errors and unexpected behavior.
    """

    inventory_logger = get_logger(PathModel.inventory_logs, "inventorymanagement")

    @staticmethod
    def food_inventory_menu():
        """Displays inventory menu and routes user choices to inventory operations."""
        try:
            while True:
                print("\n" + "-" * 45)
                print("           FOOD INVENTORY MENU")
                print("-" * 45)
                print("1. Check all food stock")
                print("2. Check specific food item stock")
                print("3. Add food item")
                print("4. Update quantity of the food item")
                print("5. Delete food item")
                print("6. Exit")
                print("=" * 45)

                try:
                    choice = int(input("Enter your choice (1-6): "))
                except ValueError:
                    print("Invalid input! Only numbers are allowed.")
                    continue

                
                if choice == 1:
                    FoodInventorymanagment.check_stock()
                elif choice == 2:
                    FoodInventorymanagment.search_item()
                elif choice == 3:
                    FoodInventorymanagment.add_item()
                elif choice == 4:
                    FoodInventorymanagment.update_quantity()
                elif choice == 5:
                    FoodInventorymanagment.delete_item()
                elif choice == 6:
                    print("Exiting Inventory Management.")
                    break
                else:
                    print("Invalid choice!")
        except Exception as e:
                FoodInventorymanagment.inventory_logger.exception(
                    f"Unexpected error in menu operation | Choice: {choice} | Error: {e}"
                )
                print("There is some issue. Please try after some time.")

    @staticmethod
    def _load_inventory():
        """Loads inventory data from file and converts it into InventoryItemModel objects."""
        try:
            raw_data = Createfile(PathModel.inventory_data).file()
            inventory = []

            for data in raw_data:
                item = InventoryItemModel()
                item.name = data["name"]
                item.quantity = data["quantity"]
                item.unit = data["unit"]
                item.reorder_level = data["reorder_level"]
                item.purchase_date = data["purchase_date"]
                item.expiry_date = data["expiry_date"]
                inventory.append(item)

            return inventory
        except Exception as e:
            FoodInventorymanagment.inventory_logger.exception(f"Unexpected error in _load_inventory | Error: {e}")
            print("There is some issue. Please try after some time.")
            return []

    @staticmethod
    def _save_inventory(inventory):
        """Saves updated inventory list back to the inventory data file."""
        try:
            Createfile(PathModel.inventory_data).write_in_file(
                [item.__dict__ for item in inventory]
            )
        except Exception as e:
            FoodInventorymanagment.inventory_logger.exception(f"Unexpected error in _save_inventory | Error: {e}")
            print("There is some issue. Please try after some time.")

    @staticmethod
    def add_item():
        "Adds a new food item to inventory or updates quantity if item already exists."""
        try:
            FoodInventorymanagment.remove_expired_items()
            inventory = FoodInventorymanagment._load_inventory()
            validation_check = Validationcheck()

            name = validation_check.name_check(input("Enter food item name: ").strip(), "Enter food item name: ")

            for item in inventory:
                if item.name.lower() == name.lower():
                    print(f"'{name}' already exists.")
                    if input("Add more quantity? (y/n): ").lower() == "y":
                        item.quantity += validation_check.validate_quantity(input("Enter additional quantity: "))
                        FoodInventorymanagment._save_inventory(inventory)
                    return

            item = InventoryItemModel()
            item.name = name
            item.quantity = validation_check.validate_quantity(input("Enter quantity: "))
            item.unit = validation_check.validate_unit(input("Enter unit (kg/liters/pieces): "))
            item.reorder_level = validation_check.validate_reorder_level(input("Enter reorder level: "), item.quantity)
            item.purchase_date = validation_check.validate_purchase_date(input("Enter purchase date (YYYY-MM-DD): "))
            item.expiry_date = validation_check.validate_expiry_date(input("Enter expiry date (YYYY-MM-DD): "), item.purchase_date)

            inventory.append(item)
            FoodInventorymanagment._save_inventory(inventory)
            print(f"Food item '{name}' added successfully!")
        except Exception as e:
            FoodInventorymanagment.inventory_logger.exception(f"Unexpected error in add_item | Error: {e}")
            print("There is some issue. Please try after some time.")

    @staticmethod
    def delete_item():
        """Deletes a specified food item from the inventory."""
        try:
            FoodInventorymanagment.remove_expired_items()
            inventory = FoodInventorymanagment._load_inventory()
            validation_check = Validationcheck()

            name = validation_check.name_check(input("Enter item name to delete: ").strip(), "Enter item name: ")

            for item in inventory:
                if item.name.lower() == name.lower():
                    inventory.remove(item)
                    FoodInventorymanagment._save_inventory(inventory)
                    print(f"'{name}' deleted successfully!")
                    return

            print("Item not found.")
        except Exception as e:
            FoodInventorymanagment.inventory_logger.exception(f"Unexpected error in delete_item | Error: {e}")
            print("There is some issue. Please try after some time.")

    @staticmethod
    def update_quantity():
        """Updates the quantity of an existing food item in inventory."""
        try:
            FoodInventorymanagment.remove_expired_items()
            inventory = FoodInventorymanagment._load_inventory()
            validation_check = Validationcheck()

            name = input("Enter item name: ").strip().lower()

            for item in inventory:
                if item.name.lower() == name:
                    item.quantity = validation_check.validate_quantity(input("Enter new quantity: "))
                    FoodInventorymanagment._save_inventory(inventory)
                    print("Quantity updated successfully!")
                    return

            print("Item not found.")
        except Exception as e:
            FoodInventorymanagment.inventory_logger.exception(f"Unexpected error in update_quantity | Error: {e}")
            print("There is some issue. Please try after some time.")

    @staticmethod
    def check_stock():
        """Displays all inventory items along with stock status."""
        try:
            FoodInventorymanagment.remove_expired_items()
            inventory = FoodInventorymanagment._load_inventory()

            if not inventory:
                print("Inventory is empty.")
                return

            for item in inventory:
                print("-" * 60)
                print(f"Item Name     : {item.name}")
                print(f"Quantity      : {item.quantity} {item.unit}")
                print(f"Reorder Level : {item.reorder_level}")
                print(f"Expiry Date   : {item.expiry_date}")

                if item.quantity <= item.reorder_level:
                    print("Status        : LOW STOCK")
                else:
                    print("Status        : Available")
        except Exception as e:
           FoodInventorymanagment.inventory_logger.exception(f"Unexpected error in check_stock | Error: {e}")
           print("There is some issue. Please try after some time.")

    @staticmethod
    def remove_expired_items():
        """Removes expired food items from inventory based on expiry date."""
        try:
            inventory = FoodInventorymanagment._load_inventory()
            today = datetime.now()
            updated = []
            removed = []

            for item in inventory:
                if datetime.strptime(item.expiry_date, "%Y-%m-%d") < today:
                    removed.append(item.name)
                else:
                    updated.append(item)

            if removed:
                FoodInventorymanagment._save_inventory(updated)
                print("Expired items removed:")
                for name in removed:
                    print(f"- {name}")
        except Exception as e:
            FoodInventorymanagment.inventory_logger.exception(f"Unexpected error in remove_expired_items | Error: {e}")
            print("There is some issue. Please try after some time.")

    @staticmethod
    def search_item():
        """Searches and displays details of a specific food item."""
        try:
            FoodInventorymanagment.remove_expired_items()
            inventory = FoodInventorymanagment._load_inventory()
            validation_check = Validationcheck()

            name = validation_check.name_check(input("Enter item name: ").strip(), "Enter item name: ")

            for item in inventory:
                if item.name.lower() == name.lower():
                    print("=" * 50)
                    print(f"Item Name       : {item.name}")
                    print(f"Quantity        : {item.quantity} {item.unit}")
                    print(f"Reorder Level   : {item.reorder_level}")
                    print(f"Purchase Date   : {item.purchase_date}")
                    print(f"Expiry Date     : {item.expiry_date}")
                    if item.quantity <= item.reorder_level:
                        print("Status          : LOW STOCK")
                    else:
                        print("Status          : Available")
                    print("=" * 50)
                    return

            print("Item not found.")
        except Exception as e:
            FoodInventorymanagment.inventory_logger.exception(f"Unexpected error in search_item | Error: {e}")
            print("There is some issue. Please try after some time.")
