from .tablebooking import Booktable
from .ordersystem import Managingorders
from .billingsystem import Generatesbill
from ..model.models import PathModel
from .filehandler import Createfile

class Menustaff:

    @staticmethod
    def staffdasbord():
        while True:
            print("\n" + "="*50)
            print(" " * 15 + "STAFF MAIN DASHBOARD")
            print("="*50)
            print("1. Book Table & Take Order")
            print("2. Advance Table Booking")
            print("3. Exit")
            print("="*50)

            try:
                choice = int(input("Enter your choice (1-3): "))
            except ValueError:
                print("Invalid input! Only numbers (1-3) are allowed.")
                continue

            if choice == 1:
                print("\n" + "-"*50)
                print("   Table Booking & Order Menu")
                print("-"*50)
                Menustaff.tablebooking_takeordermenu()
            elif choice == 2:
                print("\n" + "-"*50)
                print("         Advance Table Booking")
                print("-"*50)
                ob = Booktable()
                ob.run_menu()
            elif choice == 3:
                print("Exiting Staff Dashboard. Goodbye!")
                break
            else:
                print("Invalid choice! Please select a number between 1 and 3.")

    @staticmethod
    def select_booking_option():
        while True:
            print("\n" + "-"*50)
            print("Booking Options")
            print("-"*50)
            print("1. Book Now")
            print("2. Use Advance Booking")
            print("3. Back")
            print("-"*50)

            try:
                sub_choice = int(input("Choose option (1-3): "))
            except ValueError:
                print("Invalid input! Only numbers allowed.")
                continue

            ob = Booktable()

            if sub_choice == 1:
                table_book = ob.show_current_tables_booking()
                if table_book is not None:
                    table_book = dict(table_book)
                return table_book

            elif sub_choice == 2:
                booking_id = input("Enter your Booking ID: ").strip()
                booked_data = Createfile(PathModel.table_booked).file() or []
                matched_booking = None

                for b in booked_data:
                    if b["booking_id"] == booking_id:
                        matched_booking = b
                        break

                if matched_booking:
                    print(f" Advance booking loaded for ID: {booking_id}")
                    return matched_booking
                else:
                    print(" Booking ID not found or expired!")
                    return None

            elif sub_choice == 3:
                return None
            else:
                print("Invalid option! Choose 1, 2, or 3.")

    @staticmethod
    def tablebooking_takeordermenu():
        table_book = None
        order_taken = None

        while True:
            print("\n" + "="*50)
            print(" " * 12 + "STAFF ORDER & TABLE DASHBOARD")
            print("="*50)
            print("1. Table Booking")
            print("2. Take Order")
            print("3. Generate Bill")
            print("4. Exit")
            print("="*50)

            try:
                choice = int(input("Enter your choice (1-4): "))
            except ValueError:
                print("Invalid input! Only numbers (1-4) are allowed.")
                continue

            if choice == 1:
                table_book = Menustaff.select_booking_option()

            elif choice == 2:
                if table_book is None:
                    print("⚠️ Please do booking first!")
                else:
                    Managingorders.order_menu()
                    order_taken = list(Managingorders.order_data) if Managingorders.order_data else []

            elif choice == 3:
                if order_taken and table_book:  
                    print("\n" + "-"*50)
                    print("Generating Bill...")
                    print("-"*50)
                    Generatesbill(order_taken, table_book).show_bill()
                    table_book = None
                    order_taken = None
                    Managingorders.order_data = []
                else:
                    print("Please complete table booking and order before generating the bill!")

            elif choice == 4:
                if table_book or order_taken:
                    print("You have pending booking or order! Please generate the bill before exiting.")
                else:
                    print("Exiting Table & Order Dashboard.")
                    break
            else:
                print("Invalid choice! Please select a number between 1 and 4.")
