from ..model.models import PathModel,BookingModel,TableModel
from .filehandler import Createfile
from datetime import datetime, timedelta
from .ordersystem import Managingorders
import uuid

class Booktable:
    def __init__(self):
        table_file = Createfile(PathModel.table_data)
        raw_tables = table_file.file() or []
        self.table_data = []
        for t in raw_tables:
            table = TableModel()
            table.table_no = t["table_no"]
            table.total_seats = t["total_seats"]
            self.table_data.append(table)

        booking_file = Createfile(PathModel.table_booked)
        raw_bookings = booking_file.file() or []
        self.table_booking = []
        for booking_group in raw_bookings:
            booking_id = booking_group["booking_id"]
            created_at = booking_group["created_at"]

            for t in booking_group["tables"]:
                booking = BookingModel()
                booking.booking_id = booking_id
                booking.created_at = created_at
                booking.date = t["date"]
                booking.time_slot = t["time_slot"]
                booking.table_no = t["table_no"]
                booking.seats_booked = t["seats_booked"]

                self.table_booking.append(booking)


    def run_menu(self):
        while True:
            print("\n" + "="*35)
            print("Restaurant Table Booking System")
            print("="*35)
            
            print("1. Book a Table")
            print("2. View all Table Status")
            print("3. View All Bookings")
            print("4. Manually Remove Expired Bookings")
            print("5. Exit")
            print("="*35)

            try:
                choice = int(input("Enter your choice(1-5): "))
            except ValueError:
                print("Invalid input! Please enter a number only")
                continue

            if choice == 1:
                self.book_table()
            elif choice == 2:
                self.view_current_table_status()
            elif choice == 3:
                self.view_all_bookings()
            elif choice == 4:
                self.remove_expired_bookings()
            elif choice == 5:
                    break
            else:
                print("Invalid choice! Please enter a number between 1 and 5.")

    def remove_expired_bookings(self):
        now = datetime.now()
        updated_bookings = []
        changed = False  

        for booking in self.table_booking:
            booking_date = booking.date
            slot_end_str = booking.time_slot.split(" - ")[1]

            slot_end_datetime = datetime.strptime(
                f"{booking_date} {slot_end_str}",
                "%Y-%m-%d %H:%M"
            )

            if slot_end_datetime > now:
                updated_bookings.append(booking)
            else:
                changed = True

        if changed:
            self.table_booking = updated_bookings
            self.saving_tablebooking()
            print("Expired bookings removed.")

    def generate_time_slots_for_today(self, interval_hours=2):
        start_time = datetime.strptime("10:00", "%H:%M").time()
        end_time = datetime.strptime("22:00", "%H:%M").time()

        today = datetime.now().date()
        current_start = datetime.combine(today, start_time)
        service_end = datetime.combine(today, end_time)

        slots = []
        while current_start < service_end:
            current_end = current_start + timedelta(hours=interval_hours)
            if current_end > service_end:
                current_end = service_end

            slots.append(f"{current_start.strftime('%H:%M')} - {current_end.strftime('%H:%M')}")
            current_start = current_end

        return slots
    def saving_tablebooking(self):
        grouped = {}

        for b in self.table_booking:
            if b.booking_id not in grouped:
                grouped[b.booking_id] = {
                    "booking_id": b.booking_id,
                    "created_at": b.created_at,
                    "tables": []
                }

            grouped[b.booking_id]["tables"].append({
                "date": b.date,
                "time_slot": b.time_slot,
                "table_no": b.table_no,
                "seats_booked": b.seats_booked
            })

        data_to_save = list(grouped.values())
        Createfile(PathModel.table_booked).write_in_file(data_to_save)


    def get_available_slots_with_tables(self, date, all_slots):
        available_data = {}
        for slot in all_slots:
            available_tables = []

            for table in self.table_data:
                booked_seats = sum(
                    b.seats_booked for b in self.table_booking
                    if b.date == date and b.time_slot == slot and b.table_no == table.table_no
                )
                remaining_seats = table.total_seats - booked_seats
                if remaining_seats > 0:
                    available_tables.append({
                        "table_no": table.table_no,
                        "total_seats": remaining_seats
                    })

            if available_tables:
                available_data[slot] = available_tables

        return available_data

    def choose_time_slot(self, time_slots):
        for i, slot in enumerate(time_slots, start=1):
            print(f"{i}. {slot}")

        while True:
            try:
                choice = int(input(f"Choose an option (1-{len(time_slots)}) or press {len(time_slots)+1} to cancel = "))
            except ValueError:
                print("Invalid input! Only numbers are allowed.")
                continue

            if choice == len(time_slots)+1:
                return None
            elif 1 <= choice <= len(time_slots):
                return choice - 1
            else:
                print("Invalid choice!")

    def choose_table(self, tables):
        for i, table in enumerate(tables, start=1):
            print(f"{i}. Table No. = {table['table_no']} (Seats: {table['total_seats']})")

        while True:
            try:
                choice = int(input(f"Choose table (1-{len(tables)}) or press {len(tables)+1} to cancel = "))
            except ValueError:
                print("Invalid input! Only numbers are allowed.")
                continue

            if choice == len(tables)+1:
                return None
            elif 1 <= choice <= len(tables):
                return choice - 1
            else:
                print("Invalid choice!")

    def choose_seats(self, max_seats):
        while True:
            try:
                seats = int(input(f"How many seats (1-{max_seats})? "))
            except ValueError:
                print("Invalid input! Only numbers are allowed.")
                continue

            if 1 <= seats <= max_seats:
                return seats
            else:
                print("Invalid seat count!")

    def book_table(self):
        today = str(datetime.now().date())
        print(f"\n--- Advance Table Booking for {today} ---")

        all_slots = self.generate_time_slots_for_today()
        availability = self.get_available_slots_with_tables(today, all_slots)

        if not availability:
            print("No available slots for today.")
            return

        available_slots = list(availability.keys())
        time_slot_index = self.choose_time_slot(available_slots)
        if time_slot_index is None:
            print("Booking cancelled.")
            return

        selected_slot = available_slots[time_slot_index]
        table_status = availability[selected_slot]

        for t in table_status:
            booked = sum(
                b.seats_booked for b in self.table_booking
                if b.date == today
                and b.time_slot == selected_slot
                and b.table_no == t["table_no"]
            )
            t["available"] = t["total_seats"] - booked

        total_available = sum(t["available"] for t in table_status if t["available"] > 0)

        if total_available <= 0:
            print("No seats available for this slot.")
            return

        print(f"\n--- AVAILABLE TABLES ({selected_slot}) ---")
        print("-" * 60)
        for t in table_status:
            print(f"Table {t['table_no']} → Available Seats: {t['available']}")
        print("-" * 60)
        print(f"TOTAL AVAILABLE SEATS: {total_available}")

        while True:
            try:
                seats_needed = int(input("How many seats do you want to book? "))
                if 1 <= seats_needed <= total_available:
                    break
                print("Invalid seat count!")
            except ValueError:
                print("Enter numbers only!")

        booking_id = uuid.uuid4().hex[:6]
        seats_booked_total = 0


        while seats_booked_total < seats_needed:
            remaining = seats_needed - seats_booked_total
            print(f"\nSeats remaining to book: {remaining}")

            try:
                table_no = int(input("Enter table number: "))
            except ValueError:
                print("Invalid input!")
                continue

            table = next((t for t in table_status if t["table_no"] == table_no), None)
            if not table or table["available"] == 0:
                print("Invalid or full table!")
                continue

            max_seats = min(table["available"], remaining)

            try:
                seats = int(input(f"Seats to book (1-{max_seats}): "))
            except ValueError:
                print("Invalid input!")
                continue

            if seats < 1 or seats > max_seats:
                print("Invalid seat count!")
                continue

            booking = BookingModel()
            booking.booking_id = booking_id
            booking.date = today
            booking.time_slot = selected_slot
            booking.table_no = table_no
            booking.seats_booked = seats
            booking.created_at = datetime.now().isoformat()

            self.table_booking.append(booking)

            table["available"] -= seats
            seats_booked_total += seats

            print(f"{seats} seats booked on Table {table_no}")

        self.saving_tablebooking()

        print("\n BOOKING COMPLETED SUCCESSFULLY")
        print(f"Booking ID : {booking_id}")
        print(f"Time Slot  : {selected_slot}")
        print(f"Total Seats Booked : {seats_booked_total}")
        print("-------------------------------------------------------------\n")


    def view_all_bookings(self):
        if not self.table_booking:
            print("\nNo bookings found.")
            return

        print("\n" + "=" * 60)
        print(f"{'ALL BOOKINGS':^60}")
        print("=" * 60)

        grouped_bookings = {}

        for b in self.table_booking:
            if b.booking_id not in grouped_bookings:
                grouped_bookings[b.booking_id] = {
                    "date": b.date,
                    "time_slot": b.time_slot,
                    "tables": []
                }

            grouped_bookings[b.booking_id]["tables"].append({
                "table_no": b.table_no,
                "seats_booked": b.seats_booked
            })

        for booking_id, data in grouped_bookings.items():
            print(f"\nBooking ID : {booking_id}")
            print(f"Date       : {data['date']}")
            print(f"Time Slot  : {data['time_slot']}")
            print("-" * 60)
            print(f"{'Table No':^10}|{'Seats Booked':^15}")
            print("-" * 60)

            for t in data["tables"]:
                print(f"{t['table_no']:^10}|{t['seats_booked']:^15}")

            print("-" * 60)


    def view_current_table_status(self):
        today = str(datetime.now().date())
        print("\n" + "=" * 60)
        print(f"{'CURRENT TABLE STATUS':^60}")
        print(f"{today:^60}")
        print("=" * 60)

        all_slots = self.generate_time_slots_for_today()
        if not all_slots:
            print("No slots available for today.")
            return

        print("\nAvailable Time Slots:")
        for i, slot in enumerate(all_slots, start=1):
            print(f"  {i}. {slot}")

        while True:
            try:
                choice = int(input(f"\nChoose slot (1-{len(all_slots)}) or 0 to go back = "))
            except ValueError:
                print("Invalid input! Only numbers allowed.")
                continue

            if choice == 0:
                print("exit form viwe table status.")
                return
            elif 1 <= choice <= len(all_slots):
                selected_slot = all_slots[choice - 1]
                break
            else:
                print("Invalid choice!")

        print("\n" + "-" * 60)
        print(f"{'Time Slot: ' + selected_slot:^60}")
        print("-" * 60)

        header = f"{'Table No':^10}|{'Total Seats':^15}|{'Booked':^10}|{'Available':^12}"
        print(header)
        print("-" * 60)

        total_available = 0

        for table in self.table_data:
            booked_seats = sum(
                b.seats_booked for b in self.table_booking
                if b.date == today
                and b.time_slot == selected_slot
                and b.table_no == table.table_no
            )

            available_seats = max(table.total_seats - booked_seats, 0)
            total_available += available_seats

            print(
                f"{table.table_no:^10}|"
                f"{table.total_seats:^15}|"
                f"{booked_seats:^10}|"
                f"{available_seats:^12}"
            )

        print("-" * 60)
        print(f"{'TOTAL AVAILABLE SEATS':<30}: {total_available}")
        print("=" * 60 + "\n")

    def show_current_tables_booking(self):
        today = str(datetime.now().date())
        current_time = datetime.now().time()

        all_slots = self.generate_time_slots_for_today()
        matched_slot = None

        for slot in all_slots:
            start_str, end_str = slot.split(" - ")
            start_time = datetime.strptime(start_str, "%H:%M").time()
            end_time = datetime.strptime(end_str, "%H:%M").time()

            if start_time <= current_time < end_time:
                matched_slot = slot
                break

        if not matched_slot:
            print("No active table slot at this time.")
            return
        
        table_status = []
        total_available = 0

        for table in self.table_data:
            booked_seats = sum(
                b.seats_booked for b in self.table_booking
                if b.date == today
                and b.time_slot == matched_slot
                and b.table_no == table.table_no
            )

            available = table.total_seats - booked_seats
            if available > 0:
                table_status.append({
                    "table_no": table.table_no,
                    "available": available
                })
                total_available += available

        if total_available == 0:
            print("No seats available at this time.")
            return

    
        print(f"\n--- CURRENT TABLE STATUS ({matched_slot}) ---")
        print("-" * 60)
        for t in table_status:
            print(f"Table {t['table_no']} → Available Seats: {t['available']}")
        print("-" * 60)
        print(f"TOTAL AVAILABLE SEATS: {total_available}")

    
        while True:
            try:
                seats_needed = int(input("How many seats do you want to book? "))
                if 1 <= seats_needed <= total_available:
                    break
                print("Invalid seat count!")
            except ValueError:
                print("Enter numbers only!")

        seats_booked_total = 0
        booking_id = uuid.uuid4().hex[:6]

        selected_tables = []
        while seats_booked_total < seats_needed:
            remaining = seats_needed - seats_booked_total
            print(f"\nSeats remaining to book: {remaining}")

            table_no = int(input("Enter table number: "))

            table = next((t for t in table_status if t["table_no"] == table_no), None)
            if not table:
                print("Invalid table number!")
                continue

            max_seats = min(table["available"], remaining)

            try:
                seats = int(input(f"Seats to book (1-{max_seats}): "))
            except ValueError:
                print("Invalid input!")
                continue

            if seats < 1 or seats > max_seats:
                print("Invalid seat count!")
                continue

            booking = BookingModel()
            booking.booking_id = booking_id
            booking.date = today
            booking.time_slot = matched_slot
            booking.table_no = table_no
            booking.seats_booked = seats
            booking.created_at = datetime.now().isoformat()

            self.table_booking.append(booking)

            selected_tables.append({
            "table_no": table_no,
            "seats_booked": seats
                })

            table["available"] -= seats
            seats_booked_total += seats

            print(f"{seats} seats booked on Table {table_no}")

        self.saving_tablebooking()

        print("\n BOOKING COMPLETED SUCCESSFULLY")
        print(f"Booking ID : {booking_id}")
        print(f"Time Slot  : {matched_slot}")
        print(f"Total Seats Booked : {seats_booked_total}")
        booking_summary = {
        "booking_id": booking_id,
        "date": today,
        "time_slot": matched_slot,
        "total_seats_booked": seats_booked_total,
        "tables": selected_tables
        }

        return booking_summary