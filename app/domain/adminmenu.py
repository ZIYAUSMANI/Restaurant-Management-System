from ..menu.menusystem import Menumanagment
class Menuadmin:
    @staticmethod
    def admindasbord():
        while True:
            print("\n" + "="*45)
            print("           ADMIN MAIN DASHBOARD")
            print("="*45)
            print("1. Menu Management")
            print("2. Staff Management")
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
                print("\n--- Menu Management ---")
                Menumanagment.manage_menu()
            elif choice == 2:
                print("\n--- Staff Management ---")
            elif choice == 3:
                print("\n--- Inventory Management ---")
            elif choice == 4:
                print("\n--- Report System ---")
            elif choice == 5:
                print("Exiting Admin Dashboard. Goodbye!")
                break
            else:
                print("Invalid choice! Please select a number between 1 and 5.")
