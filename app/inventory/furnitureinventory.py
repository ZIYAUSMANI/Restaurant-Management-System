from ..domain.filehandler import Createfile
from ..model.models import PathModel, FurnitureItemModel
from ..validation.checkvalidation import Validationcheck
from ..logs.logger import get_logger
from datetime import datetime


class FurnitureInventoryManagement:
    """
    FurnitureInventoryManagement handles complete furniture inventory operations.
    It allows adding, updating, deleting, searching, and checking furniture stock.
    Inventory data is stored in files and validated using Validationcheck.
    Logging is used to track errors and unexpected behavior.
    """

    furniture_logger = get_logger(PathModel.inventory_logs, "furnitureinventory")

  
    def furniture_inventory_menu():
        """Displays furniture inventory menu and routes user choices."""
        try:
            while True:
                print("\n" + "-" * 50)
                print("        FURNITURE INVENTORY MENU")
                print("-" * 50)
                print("1. Check all furniture stock")
                print("2. Search furniture item")
                print("3. Add furniture item")
                print("4. Update furniture quantity")
                print("5. Delete furniture item")
                print("6. Exit")
                print("=" * 50)

                try:
                    choice = int(input("Enter your choice (1-6): "))
                except ValueError:
                    print("Invalid input! Only numbers are allowed.")
                    continue

                if choice == 1:
                    FurnitureInventoryManagement.check_stock()
                elif choice == 2:
                    FurnitureInventoryManagement.search_item()
                elif choice == 3:
                    FurnitureInventoryManagement.add_item()
                elif choice == 4:
                    FurnitureInventoryManagement.update_quantity()
                elif choice == 5:
                    FurnitureInventoryManagement.delete_item()
                elif choice == 6:
                    print("Exiting Furniture Inventory.")
                    break
                else:
                    print("Invalid choice!")
        except Exception as e:
            FurnitureInventoryManagement.furniture_logger.exception(
                f"Unexpected error in furniture_inventory_menu | Error: {e}"
            )
            print("There is some issue. Please try after some time.")



    @staticmethod
    def _load_inventory():
        """Loads furniture inventory data from file."""
        try:
            raw_data = Createfile(PathModel.furniture_inventory_data).file()
            inventory = []

            for data in raw_data:
                item = FurnitureItemModel()
                item.name = data["name"]
                item.quantity = data["quantity"]
                item.material = data["material"]
                item.reorder_level = data["reorder_level"]
                item.purchase_date = data["purchase_date"]
                item.warranty_end = data["warranty_end"]
                inventory.append(item)

            return inventory
        except Exception as e:
            FurnitureInventoryManagement.furniture_logger.exception(
                f"Unexpected error in _load_inventory | Error: {e}"
            )
            print("There is some issue. Please try after some time.")
            return []

    @staticmethod
    def _save_inventory(inventory):
        """Saves updated furniture inventory back to file."""
        try:
            Createfile(PathModel.furniture_inventory_data).write_in_file(
                [item.__dict__ for item in inventory]
            )
        except Exception as e:
            FurnitureInventoryManagement.furniture_logger.exception(
                f"Unexpected error in _save_inventory | Error: {e}"
            )
            print("There is some issue. Please try after some time.")


    @staticmethod
    def add_item():
        """Adds a new furniture item or updates quantity if it exists."""
        try:
            FurnitureInventoryManagement.remove_expired_items()
            inventory = FurnitureInventoryManagement._load_inventory()
            validation = Validationcheck()

            name = validation.name_check(
                input("Enter furniture name: ").strip(),
                "Enter furniture name: "
            )

            for item in inventory:
                if item.name.lower() == name.lower():
                    print(f"'{name}' already exists.")
                    if input("Add more quantity? (y/n): ").lower() == "y":
                        item.quantity += validation.validate_quantity(
                            input("Enter additional quantity: ")
                        )
                        FurnitureInventoryManagement._save_inventory(inventory)
                    return

            item = FurnitureItemModel()
            item.name = name
            item.quantity = validation.validate_quantity(input("Enter quantity: "))
            item.material = validation.validate_material(input("Enter material (wood/metal/plastic/glass): "))
            item.reorder_level = validation.validate_reorder_level(input("Enter reorder level: "), item.quantity)
            item.purchase_date = validation.validate_purchase_date(input("Enter purchase date (YYYY-MM-DD): "))
            item.warranty_end = validation.validate_expiry_date(input("Enter warranty end date (YYYY-MM-DD): "),item.purchase_date)

            inventory.append(item)
            FurnitureInventoryManagement._save_inventory(inventory)
            print(f"Furniture item '{name}' added successfully!")

        except Exception as e:
            FurnitureInventoryManagement.furniture_logger.exception(
                f"Unexpected error in add_item | Error: {e}"
            )
            print("There is some issue. Please try after some time.")


    @staticmethod
    def delete_item():
        """Deletes a furniture item from inventory."""
        try:
            FurnitureInventoryManagement.remove_expired_items()
            inventory = FurnitureInventoryManagement._load_inventory()
            validation = Validationcheck()

            name = validation.name_check(
                input("Enter furniture name to delete: ").strip(),
                "Enter furniture name: "
            )

            for item in inventory:
                if item.name.lower() == name.lower():
                    inventory.remove(item)
                    FurnitureInventoryManagement._save_inventory(inventory)
                    print(f"'{name}' deleted successfully!")
                    return

            print("Furniture not found.")
        except Exception as e:
            FurnitureInventoryManagement.furniture_logger.exception(
                f"Unexpected error in delete_item | Error: {e}"
            )
            print("There is some issue. Please try after some time.")


    @staticmethod
    def update_quantity():
        """Updates quantity of an existing furniture item."""
        try:
            FurnitureInventoryManagement.remove_expired_items()
            inventory = FurnitureInventoryManagement._load_inventory()
            validation = Validationcheck()

            name = input("Enter furniture name: ").strip().lower()

            for item in inventory:
                if item.name.lower() == name:
                    item.quantity = validation.validate_quantity(
                        input("Enter new quantity: ")
                    )
                    FurnitureInventoryManagement._save_inventory(inventory)
                    print("Quantity updated successfully!")
                    return

            print("Furniture not found.")
        except Exception as e:
            FurnitureInventoryManagement.furniture_logger.exception(
                f"Unexpected error in update_quantity | Error: {e}"
            )
            print("There is some issue. Please try after some time.")

    @staticmethod
    def check_stock():
        """Displays all furniture stock with status."""
        try:
            FurnitureInventoryManagement.remove_expired_items()
            inventory = FurnitureInventoryManagement._load_inventory()

            if not inventory:
                print("Furniture inventory is empty.")
                return

            for item in inventory:
                print("-" * 60)
                print(f"Furniture Name : {item.name}")
                print(f"Quantity       : {item.quantity}")
                print(f"Material       : {item.material}")
                print(f"Reorder Level  : {item.reorder_level}")
                print(f"Warranty End   : {item.warranty_end}")

                if item.quantity <= item.reorder_level:
                    print("Status         : LOW STOCK")
                else:
                    print("Status         : Available")
        except Exception as e:
            FurnitureInventoryManagement.furniture_logger.exception(
                f"Unexpected error in check_stock | Error: {e}"
            )
            print("There is some issue. Please try after some time.")

    @staticmethod
    def search_item():
        """Searches and displays a specific furniture item."""
        try:
            FurnitureInventoryManagement.remove_expired_items()
            inventory = FurnitureInventoryManagement._load_inventory()
            validation = Validationcheck()

            name = validation.name_check(
                input("Enter furniture name: ").strip(),
                "Enter furniture name: "
            )

            for item in inventory:
                if item.name.lower() == name.lower():
                    print("=" * 50)
                    print(f"Furniture Name : {item.name}")
                    print(f"Quantity       : {item.quantity}")
                    print(f"Material       : {item.material}")
                    print(f"Purchase Date  : {item.purchase_date}")
                    print(f"Warranty End   : {item.warranty_end}")
                    print("=" * 50)
                    return

            print("Furniture not found.")
        except Exception as e:
            FurnitureInventoryManagement.furniture_logger.exception(
                f"Unexpected error in search_item | Error: {e}"
            )
            print("There is some issue. Please try after some time.")
        
    

    @staticmethod
    def remove_expired_items():
        """
        Removes furniture items whose warranty has expired.
        """
        try:
            inventory = FurnitureInventoryManagement._load_inventory()
            today = datetime.now()
            updated_inventory = []
            removed_items = []

            for item in inventory:
                if datetime.strptime(item.warranty_end, "%Y-%m-%d") < today:
                    removed_items.append(item.name)
                else:
                    updated_inventory.append(item)

            if removed_items:
                FurnitureInventoryManagement._save_inventory(updated_inventory)
                print("Expired furniture items removed:")
                for name in removed_items:
                    print(f"- {name}")

        except Exception as e:
            FurnitureInventoryManagement.furniture_logger.exception(
                f"Unexpected error in remove_expired_items | Error: {e}"
            )
            print("There is some issue. Please try after some time.")

