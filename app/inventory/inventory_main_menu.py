from ..logs.logger import get_logger
from ..model.models import PathModel
from .foodinventory import FoodInventorymanagment
from .furnitureinventory import FurnitureInventoryManagement


class InventoryMainMenu:
    """
    InventoryMainMenu controls navigation between
    Food Inventory and Furniture Inventory systems.
    """

    main_logger = get_logger(PathModel.inventory_logs, "inventorymainmenu")

    @staticmethod
    def main_menu():
        try:
            while True:
                print("\n" + "=" * 60)
                print("        INVENTORY MANAGEMENT SYSTEM")
                print("=" * 60)
                print("1. Food Inventory")
                print("2. Furniture Inventory")
                print("3. Exit")
                print("=" * 60)

                try:
                    choice = int(input("Enter your choice (1-3): "))
                except ValueError:
                    print("Invalid input! Only numbers allowed.")
                    continue

                if choice == 1:
                    FoodInventorymanagment.food_inventory_menu()

                elif choice == 2:
                    FurnitureInventoryManagement.furniture_inventory_menu()

                elif choice == 3:
                    print("Exiting Inventory Management System.")
                    break

                else:
                    print("Invalid choice! Please select 1-3.")

        except Exception as e:
            InventoryMainMenu.main_logger.exception(
                f"Unexpected error in InventoryMainMenu | Error: {e}"
            )
            print("There is some issue. Please try after some time.")
