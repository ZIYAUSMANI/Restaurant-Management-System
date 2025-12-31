from ..model.models import PathModel,BookingModel,TableModel
from .filehandler import Createfile
from datetime import datetime, timedelta
from .ordermanagment import Managingorders
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
        for b in raw_bookings:
            booking = BookingModel()
            booking.booking_id = b["booking_id"]
            booking.date = b["date"]
            booking.time_slot = b["time_slot"]
            booking.table_no = b["table_no"]
            booking.seats_booked = b["seats_booked"]
            booking.created_at = b["created_at"]
            self.table_booking.append(booking)

        self.booking_data = {}

    def run_menu(self):
        while True:
            print("\n" + "="*35)
            print("Restaurant Table Booking System")
            print("="*35)
            
            print("1. Book a Table")
            print("2. View Current Table Status")
            print("3. View All Bookings (Debug)")
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
                if len(self.booking_data)==0:
                    print("Exiting book table system.")
                    break
                else:
                    print("Exiting book table system. going to order menu")
                    Managingorders.order_menu()
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
        data_to_save = []
        for b in self.table_booking:
            data_to_save.append({
                "booking_id": b.booking_id,
                "date": b.date,
                "time_slot": b.time_slot,
                "table_no": b.table_no,
                "seats_booked": b.seats_booked,
                "created_at": b.created_at
            })
        file = Createfile(PathModel.table_booked)
        file.write_in_file(data_to_save)

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
        print(f"\n--- Table Booking for {today} ---")

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
        available_tables = availability[selected_slot]

        print(f"\nAvailable Tables for Slot: {selected_slot}")
        table_index = self.choose_table(available_tables)
        if table_index is None:
            print("Booking cancelled.")
            return

        selected_table = available_tables[table_index]
        seats = self.choose_seats(selected_table["total_seats"])

        booking_id = uuid.uuid4().hex[:6]
        new_booking = BookingModel()
        new_booking.booking_id = booking_id
        new_booking.date = today
        new_booking.time_slot = selected_slot
        new_booking.table_no = selected_table["table_no"]
        new_booking.seats_booked = seats
        new_booking.created_at = datetime.now().isoformat()

        self.table_booking.append(new_booking)
        self.booking_data = {
        "booking_id": new_booking.booking_id,
        "date": new_booking.date,
        "time_slot": new_booking.time_slot,
        "table_no": new_booking.table_no,
        "seats_booked": new_booking.seats_booked,
        "created_at": new_booking.created_at
        }
        Managingorders.current_booking= self.booking_data
        self.saving_tablebooking()

        print("\nBOOKING CONFIRMED")
        print(f"Table No : {new_booking.table_no}")
        print(f"Seats    : {new_booking.seats_booked}")
        print(f"Time     : {new_booking.time_slot}")
        print(f"Booking ID : {new_booking.booking_id}")
        print("-------------------------------------------------------------\n")

    def view_all_bookings(self):
        if not self.table_booking:
            print("\nNo bookings found.")
            return

        print("\n--- ALL CURRENT BOOKINGS ---")
        print("-" * 70)
        print(f"{'Booking ID':<12}{'Date':<12}{'Time Slot':<15}{'Table':<8}{'Seats':<8}")
        print("-" * 70)

        for b in self.table_booking:
            print(
                f"{b.booking_id:<12}"
                f"{b.date:<12}"
                f"{b.time_slot:<15}"
                f"{b.table_no:<8}"
                f"{b.seats_booked:<8}"
            )
        print("-" * 70)

    def view_current_table_status(self):
        today = str(datetime.now().date())
        print(f"\n--- CURRENT TABLE STATUS FOR {today} ---")

        all_slots = self.generate_time_slots_for_today()
        if not all_slots:
            print("No slots available for today.")
            return

        print("\nAvailable Time Slots:")
        for i, slot in enumerate(all_slots, start=1):
            print(f"{i}. {slot}")

        while True:
            try:
                choice = int(input(f"Choose slot (1-{len(all_slots)}) or 0 to cancel = "))
            except ValueError:
                print("Invalid input! Only numbers allowed.")
                continue

            if choice == 0:
                print("View cancelled.")
                return
            elif 1 <= choice <= len(all_slots):
                selected_slot = all_slots[choice - 1]
                break
            else:
                print("Invalid choice!")

        print(f"\nTime Slot: {selected_slot}")
        print("-" * 60)
        print(f"{'Table No':<10}{'Total Seats':<15}{'Booked':<10}{'Available':<10}")
        print("-" * 60)

        for table in self.table_data:
            booked_seats = sum(
                b.seats_booked for b in self.table_booking
                if b.date == today and b.time_slot == selected_slot and b.table_no == table.table_no
            )
            available_seats = max(table.total_seats - booked_seats, 0)

            print(f"{table.table_no:<10}{table.total_seats:<15}{booked_seats:<10}{available_seats:<10}")

        print("-" * 60)
