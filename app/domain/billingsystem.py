from .filehandler import Createfile
from ..model.models import PathModel, BillItemModel
from datetime import datetime
from ..validation.checkvalidation import Validationcheck
from ..logs.logger import get_logger
class Generatesbill:
    """
    Generatesbill handles bill preparation, display, and storage.
    It calculates item totals, seat charges, GST, and grand total
    based on orders and table bookings.
    """
    bill_logger = get_logger(PathModel.bill_logs, "billing")
    def __init__(self, order_taken=None, booking_data=None):
        """
        Initializes bill generation with order and booking details.
        :param order_taken: List of order objects selected by customer
        :param booking_data: Table booking information (if any)
        """
        try:
            self.billdata = Createfile(PathModel.bill_data).file()
            self.food_data = Createfile(PathModel.food_data).file()
            self.order_taken = order_taken if order_taken else []
            self.table_booked = [booking_data] if booking_data else []
            self.bill_items = []
            self.PAYMENT_OPTIONS = {
                "1": "Cash",
                "2": "UPI",
                "3": "Credit Card",
                "4": "Debit Card"
            }
        except Exception as e:
            Generatesbill.bill_logger.exception(f"UNEXPECTED ERROR IN Generatesbill| Error: {e}")
            print("There is an issue. Please try again after some time.")

    def prepare_bill_items(self):
        """
        Prepares bill items by:
        - Calculating seat charges
        - Matching ordered items with food data
        - Calculating price, quantity, and total per item
        """
        try:
            seat_charge = 0
            for booking in self.table_booked:
                for table in booking.get("tables", []):
                    seat_charge += int(table.get("seats_booked", 0)) * 50

            for order in self.order_taken:
                order_id = getattr(order, "id", None)
                order_qty = int(getattr(order, "quantity", 0))
                order_size = getattr(order, "size_choice", "").lower()

                for category in self.food_data[0].values():
                    for items in category.values():
                        for item in items:
                            if not isinstance(item, dict):
                                continue

                            sizes = []
                            if "size" in item:
                                sizes = item["size"]
                            elif "half_price" in item and "full_price" in item:
                                sizes = [
                                    {"name": "Half", "price": item["half_price"]},
                                    {"name": "Full", "price": item["full_price"]}
                                ]
                            else:
                                sizes = [{"name": "", "price": item.get("price", 0)}]

                            price = 0
                            for s in sizes:
                                if s["name"].lower() == order_size or order_size == "":
                                    price = int(s.get("price", 0))
                                    break

                            if item.get("id") == order_id:
                                bill = BillItemModel()
                                bill.id = item["id"]
                                bill.item_name = item["item_name"]
                                bill.quantity = order_qty
                                bill.price = price
                                bill.total = bill.quantity * bill.price
                                bill.seats = seat_charge
                                self.bill_items.append(bill)
                                break
        except Exception as e:
            Generatesbill.bill_logger.exception(f"UNEXPECTED ERROR IN Generatesbill| Error: {e}")
            print("There is an issue. Please try again after some time.")

    
    def choose_payment_method(self):
        """
        Ask user to choose payment method and provide details if required.
        Returns: (payment_method:str, payment_details:dict)
        """
        try:
            validation_check=Validationcheck()
            print("\nChoose Payment Method:")
            for key, method in self.PAYMENT_OPTIONS.items():
                print(f"{key}. {method}")

            choice = input("Enter your choice (1-4): ").strip()
            payment_method = self.PAYMENT_OPTIONS.get(choice, "Cash")
            payment_details = {}

            if payment_method == "UPI":
                upi_id = validation_check.validate_upi(input("Enter UPI ID: ").strip())
                payment_details = {"upi_id": upi_id}
            elif payment_method in ("Credit Card", "Debit Card"):
                card_name = validation_check.name_check(input("Enter Cardholder Name: ").strip(),"Enter Cardholder Name:")
                card_number = validation_check.validate_card_number(input("Enter Card Number: ").strip())
                expiry_date = validation_check.validate_expiry_date(input("Enter Expiry Date (MM/YY): ").strip())
                cvv = validation_check.validate_cvv(input("Enter CVV: ").strip())
                payment_details = {
                    "card_name": card_name,
                    "card_number": card_number,
                    "expiry_date": expiry_date,
                    "cvv": cvv
                }

            confirm = input("Confirm payment? (yes/no): ").strip().lower()
            if confirm not in ("yes", "y"):
                print("Payment cancelled.")
                return None, None

            print("Payment successful ")
            return payment_method, payment_details
        except Exception as e:
            Generatesbill.bill_logger.exception(f"UNEXPECTED ERROR IN Generatesbill| Error: {e}")
            print("There is an issue. Please try again after some time.")

    def show_bill(self):
        """
        Displays the formatted bill on the console.
        Includes date, time, item details, subtotal, GST, seat charge,
        and grand total. Also triggers bill saving,handles payment,
        and saves the bill including payment info.
        """
        try:
            self.prepare_bill_items()

            now = datetime.now()
            date = now.strftime("%d-%m-%Y")
            time = now.strftime("%I:%M %p")

            payment_method, payment_details = self.choose_payment_method()
            if not payment_method:
                print("Bill generation cancelled due to payment not confirmed.")
                return

            print("\n" + "=" * 60)
            print(" " * 28 + "YOUR BILL")
            print("=" * 60)
            print(f"Date : {date}")
            print(f"Time : {time}")
            print(f"Payment Method : {payment_method}")

            if payment_method == "UPI":
                print(f"UPI ID : {payment_details.get('upi_id')}")
                
            elif payment_method in ("Credit Card", "Debit Card"):
                print(f"Cardholder Name : {payment_details.get('card_name')}")
                print(f"Card Number : {payment_details.get('card_number')}")
                print(f"Expiry Date : {payment_details.get('expiry_date')}")
            print("-" * 60)
            print(f"{'ID':<5}{'Item Name':<25}{'Qty':<8}{'Price':<10}{'Total'}")
            print("-" * 60)

            subtotal = 0
            for bill in self.bill_items:
                subtotal += bill.total
                print(f"{bill.id:<5}{bill.item_name:<25}{bill.quantity:<8}{bill.price:<10}{bill.total}")

            seat_charge = self.bill_items[0].seats if self.bill_items else 0
            if seat_charge > 0:
                print("-" * 60)
                print(f"{'Table Seat Charge':<48}\u20B9{seat_charge}")

            print("-" * 60)
            print(f"{'Subtotal':<48}\u20B9{subtotal}")
            gst = int(subtotal * 0.05)
            print(f"{'GST (5%)':<48}\u20B9{gst}")
            print("-" * 60)
            grand_total = subtotal + gst + seat_charge
            print(f"{'Grand Total':<48}\u20B9{grand_total}")
            print("=" * 60)
            print("        Thank You! Please Visit Again (^_^)")
            print("=" * 60)

            self.save_bill(date, time, subtotal, gst, grand_total, payment_method, payment_details)
        except Exception as e:
            Generatesbill.bill_logger.exception(f"UNEXPECTED ERROR IN Generatesbill| Error: {e}")
            print("There is an issue. Please try again after some time.")

    def save_bill(self, date, time, subtotal, gst, grand_total, payment_method, payment_details):
        """
            Saves the bill into the JSON file including payment details.
            """
        try:
            bill_data = {
                "date": date,
                "time": time,
                "payment_method": payment_method,
                "payment_details": payment_details,
                "items": [
                    {
                        "id": bill.id,
                        "item_name": bill.item_name,
                        "quantity": bill.quantity,
                        "price": bill.price,
                        "total": bill.total
                    } for bill in self.bill_items
                ],
                "seat_charge": self.bill_items[0].seats if self.bill_items else 0,
                "subtotal": subtotal,
                "gst": gst,
                "grand_total": grand_total
            }

            self.billdata.append(bill_data)
            Createfile(PathModel.bill_data).write_in_file(self.billdata)
        except Exception as e:
            Generatesbill.bill_logger.exception(f"UNEXPECTED ERROR IN Generatesbill| Error: {e}")
            print("There is an issue. Please try again after some time.")
