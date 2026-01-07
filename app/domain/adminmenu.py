from ..menu.menusystem import Menumanagment
from ..domain.ordermanagment import Ordermanaingsystem
from ..report.report import ReportGenerator
from ..inventory.inventory_main_menu import InventoryMainMenu
from ..model.models import PathModel
from ..logs.logger import get_logger
class Menuadmin:
    """
    Admin dashboard for managing the restaurant system.
    Provides options for menu, order, inventory, and report management.
    Handles admin choices and delegates tasks to appropriate modules.
    Logs unexpected errors using admin_logger.
    """
    admin_logger = get_logger(PathModel.admin_menu_logs, "adminmenu")
    @staticmethod
    def admindasbord():
        try:
            while True:
                print("\n" + "="*45)
                print("           ADMIN MAIN DASHBOARD")
                print("="*45)
                print("1. Menu Management")
                print("2. order Management")
                print("3. Inventory Management")
                print("4. Report System")
                print("5. Exit")
                print("="*45)

                try:
                    choice = int(input("Enter your choice (1-5): "))
                except ValueError:
                    print("Invalid input! Only numbers are allowed (1-5).")
                    continue

                if choice == 1:
                    Menumanagment.manage_menu()
                elif choice == 2:
                    Ordermanaingsystem.order_managment()
                elif choice == 3:
                    InventoryMainMenu.main_menu()
                elif choice == 4:
                    ReportGenerator.report_menu()
                elif choice == 5:
                    print("Exiting Admin Dashboard. Goodbye!")
                    break
                else:
                    print("Invalid choice! Please select a number between 1 and 5.")
        except Exception as e:
            Menuadmin.admin_logger.exception(f"Unexpected error in staff menu | Error: {e}")
            print("There is an issue. Please try again after some time.")

