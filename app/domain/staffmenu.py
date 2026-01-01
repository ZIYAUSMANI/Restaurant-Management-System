from .ordersystem import Managingorders

class Menustaff:
    @staticmethod
    def staffdasbord():
        table = None
        while True:
            print("\n" + "="*40)
            print("         STAFF MAIN DASHBOARD")
            print("="*40)
            print("1. Packed Order")
            print("2. Book Table")
            print("3. Exit")
            print("="*40)

            try:
                choice = int(input("Enter your choice (1-3): "))
            except ValueError:
                print("Invalid input! Only numbers are allowed (1-3).")
                continue

            if choice == 1:
                print("\n--- Order Menu ---")
                Managingorders.order_menu()
            elif choice == 2:
                print("\n--- Table Booking ---")
            elif choice == 3:
                print("Exiting Staff Dashboard. Goodbye!")
                break
            else:
                print("Invalid choice! Please select a number between 1 and 3.")
