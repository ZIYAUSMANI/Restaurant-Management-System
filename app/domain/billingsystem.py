from .filehandler import Createfile
from ..model.models import PathModel, BillItemModel
from datetime import datetime

class Generatesbill:
    def __init__(self, order_taken=None, booking_data=None):
        self.billdata = Createfile(PathModel.bill_data).file()
        self.food_data = Createfile(PathModel.food_data).file()
        self.order_taken = order_taken if order_taken else []
        self.table_booked = [booking_data] if booking_data else []
        self.bill_items = []

    def prepare_bill_items(self):
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

    def show_bill(self):
       
        self.prepare_bill_items()

    

        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%I:%M %p")

        print("=" * 60)
        print(" " * 28 + "YOUR BILL")
        print("=" * 60)
        print(f"Date : {date}")
        print(f"Time : {time}")
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

        self.save_bill(date, time, subtotal, gst, grand_total)

    def save_bill(self, date, time, subtotal, gst, grand_total):
        bill_data = {
            "date": date,
            "time": time,
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
