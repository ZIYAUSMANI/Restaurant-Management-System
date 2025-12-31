from .filehandler import Createfile
from ..model.models import PathModel
from datetime import datetime
from ..model.models import BillItemModel

class Generatesbill:
    def __init__(self, order_obj,booking_data=None):
        foodmenu = Createfile(PathModel.food_data)
        self.billdata = Createfile(PathModel.bill_data).file()
        self.food_data = foodmenu.file()
        self.bill_items = []
        self.order_taken = order_obj.order_data
        self.table_booked = [booking_data] if booking_data else []
      

    def prepare_bill_items(self):
        seat_charge = 0

        for booking in self.table_booked:
            seat_charge += int(booking["seats_booked"]) * 50

        for order in self.order_taken:
            for section in self.food_data[0].values():
                for item in section:
                    if item["id"] == order.id:
                        bill = BillItemModel()

                        bill.id = item["id"]
                        bill.item_name = item["item_name"]
                        bill.quantity = int(order.quantity)
                        bill.price = int(item["price"])
                        bill.total = bill.quantity * bill.price
                        bill.seats = seat_charge   
                        self.bill_items.append(bill)
                        
    def show_bill(self):
        if len(self.order_taken) == 0:
            print("There is no order!")
            return
        print("Exiting Order Menu. bill genterating in process...")
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
            print(
                f"{bill.id:<5}"
                f"{bill.item_name:<25}"
                f"{bill.quantity:<8}"
                f"{bill.price:<10}"
                f"{bill.total}"
            )

        print("-" * 60)
        seat_charge = self.bill_items[0].seats if self.bill_items else 0
        if seat_charge >0:
            print("-" * 60)
            print(f"{'Table Seat Charge':<48}\u20B9{bill.seats}")
            print("-" * 60)

        print(f"{'Subtotal':<48}\u20B9{subtotal}")
        gst=int(subtotal * 0.05)
        print(f"{'GST (5%)':<48}\u20B9{gst}")
        print("-" * 60)
        grand_total=(subtotal + int(subtotal * 0.05))+bill.seats
        print(f"{'Grand Total':<48}\u20B9{grand_total}")
        print("=" * 60)
        print("        Thank You! Please Visit Again (^_^)")
        print("=" * 60)
        self.save_bill(date,time,subtotal,gst,grand_total)

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
