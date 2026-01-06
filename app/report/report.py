from datetime import datetime
from ..domain.filehandler import Createfile
from ..model.models import PathModel, BillItemModel, UserModel
from ..logs.logger import get_logger

class ReportGenerator:
    """
    dogs string:
    - Generates restaurant reports for bills, orders, tables, and staff.
    - Reads data from JSON files using Createfile and models (BillItemModel, UserModel).
    - Provides sub-menus to filter reports by daily, weekly, monthly, or yearly periods.
    - Calculates totals, most ordered items, and most booked tables.
    - Displays staff experience in a formatted report.
    - Logs all exceptions using get_logger for error tracking.
    """
    report_logger = get_logger(PathModel.report_logs, "reportgenerator")

    @staticmethod
    def report_menu():
        """dogs string: Display main report menu and handle user selections."""
        try:
            raw_bills = Createfile(PathModel.bill_data).file()
            raw_staffs = Createfile(PathModel.registration_data).file()

            bills_data = []
            for b in raw_bills:
                bill = BillItemModel()
                bill.id = b.get("id")
                bill.date = b.get("date")
                bill.time = b.get("time")
                bill.payment_method = b.get("payment_method")
                bill.grand_total = b.get("grand_total", 0)
                bill.gst = b.get("gst", 0)
                bill.items = b.get("items", [])
                bill.tables = b.get("tables", [])
                bills_data.append(bill)

            staffs_data = []
            for s in raw_staffs:
                staff = UserModel()
                staff.id = s.get("id")
                staff.name = s.get("name")
                staff.department = s.get("department")
                staff.role = s.get("role")
                staff.past_experience = s.get("past_experience")
                staffs_data.append(staff)

            while True:
                print("\n========== REPORT MENU ==========")
                print("1. Bill Report")
                print("2. Order Report")
                print("3. Table Report")
                print("4. Staff Report")
                print("5. Exit")

                choice = input("Select an option: ").strip()

                if choice == "1":
                    ReportGenerator.generic_sub_menu("BILL", bills_data, ReportGenerator.bill_report)
                elif choice == "2":
                    ReportGenerator.generic_sub_menu("ORDER", bills_data, ReportGenerator.order_report)
                elif choice == "3":
                    ReportGenerator.generic_sub_menu("TABLE", bills_data, ReportGenerator.table_report)
                elif choice == "4":
                    ReportGenerator.staff_report(staffs_data)
                elif choice == "5":
                    print("Exiting Report Generator...")
                    break
                else:
                    print("Invalid choice. Try again.")

        except Exception as e:
            ReportGenerator.report_logger.exception(f"UNEXPECTED ERROR IN report_menu | Error: {e}")
            print("There is an issue. Please try again later.")

    @staticmethod
    def generic_sub_menu(report_name, data, report_func):
        """dogs string: Display a sub-menu for selecting report period (daily/weekly/monthly/yearly)."""
        try:
            while True:
                print(f"\n========== {report_name} REPORT MENU ==========")
                print("1. Daily Report")
                print("2. Weekly Report")
                print("3. Monthly Report")
                print("4. Yearly Report")
                print("5. Exit")

                choice = input("Select an option: ").strip()
                period_map = {"1": "daily", "2": "weekly", "3": "monthly", "4": "yearly"}

                if choice in period_map:
                    report_func(data, period_map[choice])
                elif choice == "5":
                    break
                else:
                    print("Invalid choice. Try again.")

        except Exception as e:
            ReportGenerator.report_logger.exception(f"UNEXPECTED ERROR IN generic_sub_menu | Error: {e}")
            print("There is an issue. Please try again later.")

    @staticmethod
    def bill_report(bills, period=None):
        """dogs string: Generate a bill report for the selected period showing totals and GST."""
        try:
            now = datetime.now()
            filtered_bills = []

            for bill in bills:
                try:
                    bill_date = datetime.strptime(bill.date, "%d-%m-%Y")
                except:
                    continue

                if (period == "daily" and bill_date.date() == now.date()) or \
                   (period == "weekly" and bill_date.isocalendar()[1] == now.isocalendar()[1] and bill_date.year == now.year) or \
                   (period == "monthly" and bill_date.year == now.year and bill_date.month == now.month) or \
                   (period == "yearly" and bill_date.year == now.year):
                    filtered_bills.append(bill)

            if not filtered_bills:
                print(f"No {period} bills found.")
                return

            print(f"\n====== BILL REPORT {period.upper()} ======")
            print(f"{'Bill ID':<10} | {'Date':<12} | {'Time':<8} | {'Payment':<10} | {'Amount'}")
            print("-" * 80)

            total_sales = 0
            total_gst = 0
            for index, bill in enumerate(filtered_bills, start=1):
                bill_id = f"BILL-{index:04d}"
                print(f"{bill_id:<10} | {bill.date:<12} | {bill.time:<8} | {bill.payment_method:<10} | ₹{bill.grand_total:.2f}")
                total_sales += bill.grand_total
                total_gst += bill.gst

            print("-" * 80)
            print(f"Total GST Collected : ₹{total_gst:.2f}")
            print(f"Total Sales        : ₹{total_sales:.2f}")

        except Exception as e:
            ReportGenerator.report_logger.exception(f"UNEXPECTED ERROR IN bill_report | Error: {e}")
            print("There is an issue. Please try again later.")

    @staticmethod
    def order_report(bills, period=None):
        """dogs string: Generate an order report listing each item sold and total amount."""
        try:
            now = datetime.now()
            filtered_bills = []

            for bill in bills:
                try:
                    bill_date = datetime.strptime(bill.date, "%d-%m-%Y")
                except:
                    continue

                if (period == "daily" and bill_date.date() == now.date()) or \
                   (period == "weekly" and bill_date.isocalendar()[1] == now.isocalendar()[1] and bill_date.year == now.year) or \
                   (period == "monthly" and bill_date.year == now.year and bill_date.month == now.month) or \
                   (period == "yearly" and bill_date.year == now.year):
                    filtered_bills.append(bill)

            if not filtered_bills:
                print(f"No {period} orders found.")
                return

            print(f"\n====== ORDER REPORT {period.upper()} ======")
            print(f"{'Order ID':<12} | {'Item Name':<20} | {'Date':<12} | {'Time':<8} | {'Price'}")
            print("-" * 80)

            order_index = 1
            total_amount = 0
            item_count = {}

            for bill in filtered_bills:
                for item in bill.items:
                    order_id = f"ORD-{order_index:04d}"
                    item_name = item.get("item_name", "N/A")
                    price = item.get("total", 0)
                    print(f"{order_id:<12} | {item_name:<20} | {bill.date:<12} | {bill.time:<8} | ₹{price:.2f}")
                    total_amount += price
                    item_count[item_name.lower()] = item_count.get(item_name.lower(), 0) + 1
                    order_index += 1

            print("-" * 80)
            print(f"Total Order Amount : ₹{total_amount:.2f}")

            if item_count:
                max_count = max(item_count.values())
                if max_count > 1:
                    print("\nMost Ordered Item(s)")
                    print("-------------------")
                    for name, count in item_count.items():
                        if count == max_count:
                            print(f"Item Name : {name.title()}")
                            print(f"Times Ordered : {count}")

        except Exception as e:
            ReportGenerator.report_logger.exception(f"UNEXPECTED ERROR IN order_report | Error: {e}")
            print("There is an issue. Please try again later.")

    @staticmethod
    def table_report(bills, period=None):
        """dogs string: Generate table booking report showing most booked tables and seats."""
        try:
            now = datetime.now()
            filtered_bills = []

            for bill in bills:
                try:
                    bill_date = datetime.strptime(bill.date, "%d-%m-%Y")
                except:
                    continue

                if (period == "daily" and bill_date.date() == now.date()) or \
                   (period == "weekly" and bill_date.isocalendar()[1] == now.isocalendar()[1] and bill_date.year == now.year) or \
                   (period == "monthly" and bill_date.year == now.year and bill_date.month == now.month) or \
                   (period == "yearly" and bill_date.year == now.year):
                    filtered_bills.append(bill)

            if not filtered_bills:
                print(f"No {period} table bookings found.")
                return

            print(f"\n====== TABLE REPORT {period.upper()} ======")
            print(f"{'Table ID':<12} | {'Table No':<10} | {'Seats':<6} | {'Date':<12} | {'Time'}")
            print("-" * 75)

            table_booking_count = {}
            table_seat_count = {}
            table_index = 1

            for bill in filtered_bills:
                for table in bill.tables:
                    table_id = f"TBL-{table_index:04d}"
                    table_no = table.get("table_no", "N/A")
                    seats = table.get("seats_booked", 0)
                    print(f"{table_id:<12} | {table_no:<10} | {seats:<6} | {bill.date:<12} | {bill.time}")

                    if table_no != "N/A":
                        table_booking_count[table_no] = table_booking_count.get(table_no, 0) + 1
                        table_seat_count[table_no] = table_seat_count.get(table_no, 0) + seats

                    table_index += 1

            eligible_tables = {t: s for t, s in table_seat_count.items() if table_booking_count.get(t, 0) > 1}

            if not eligible_tables:
                print("-" * 75)
                print("(no most booked table)")
                return

            max_seats = max(eligible_tables.values())
            print("-" * 75)
            print("Most Booked Table(s)")
            print("--------------------")
            for table_no, seats in eligible_tables.items():
                if seats == max_seats:
                    print(f"Table Number : {table_no}")
                    print(f"Total Seats  : {seats}\n")

        except Exception as e:
            ReportGenerator.report_logger.exception(f"UNEXPECTED ERROR IN table_report | Error: {e}")
            print("There is an issue. Please try again later.")

    @staticmethod
    def staff_report(staffs, period=None):
        """dogs string: Display staff report showing name, department, and past experience."""
        try:
            print(f"\n====== STAFF REPORT ======")
            print(f"{'Staff ID':<12} | {'Name':<12} | {'Dept':<15} | {'Experience'}")
            print("-" * 100)

            staff_count = 0
            for staff in staffs:
                if staff.role is None or staff.role.lower() == "admin":
                    continue
                experience = "0 year"
                if isinstance(staff.past_experience, list):
                    exp_summary = [f"{exp.get('company_name')} ({exp.get('experience')})" for exp in staff.past_experience]
                    experience = ", ".join(exp_summary)
                elif isinstance(staff.past_experience, str):
                    experience = staff.past_experience

                print(f"{staff.id:<12} | {staff.name.title():<12} | {staff.department:<15} | {experience}")
                staff_count += 1

            print("-" * 100)
            print(f"Total Staff : {staff_count}")

        except Exception as e:
            ReportGenerator.report_logger.exception(f"UNEXPECTED ERROR IN staff_report | Error: {e}")
            print("There is an issue. Please try again later.")
