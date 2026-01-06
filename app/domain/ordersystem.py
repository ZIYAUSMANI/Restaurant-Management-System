from ..validation.checkvalidation import Validationcheck
from ..model.models import OrderModel
from .filehandler import Createfile
from ..model.models import PathModel
from ..menu.foodmenu import Managingfoodmenu
from datetime import datetime
from ..logs.logger import get_logger


class Managingorders:
    """
    Managingorders class is used to handle customer order operations.

    It allows the user to:
    - View food menu
    - Add new orders
    - View current orders
    - Save orders to file

    Orders are temporarily stored in memory and saved permanently when user exits.
    """
    order_logger = get_logger(PathModel.order_log, "ordermangement")
    order_data = []

    @staticmethod
    def order_menu():
        """
        Displays the main order take menu."""

        try:
            while True:
                print("\n" + "="*35)
                print("           ORDER MENU")
                print("="*35)
                print("1. Show Food Menu")
                print("2. Add Order")
                print("3. Show All Orders")
                print("4. back")
                print("="*35)

                try:
                    choice = int(input("Enter your choice (1-4): "))
                except ValueError:
                    print("Invalid input! Please enter a number only.")
                    continue

                if choice == 1:
                    print("\n--- Food Menu ---")
                    Managingfoodmenu.show_food_menu()
                elif choice == 2:
                    print("\n--- Add New Order ---")
                    Managingorders.new_order()
                elif choice == 3:
                    print("\n--- All Orders ---")
                    Managingorders.show_all_order()
                elif choice == 4:
                    Managingorders.save_orders()
                    return Managingorders.order_data
                else:
                    print("Invalid choice! Please select a number between 1 and 4.")
        except Exception as e:
           Managingorders.order_logger.exception(
            f"UNEXPECTED ERROR IN Managingorder| Error: {e}")
           print("There is an issue. Please try again after some time.")

    @classmethod
    def save_orders(cls):
        """
        Saves all current orders to the order data file."""
        try:
            if not cls.order_data:
                return
            order_full_data = Createfile(PathModel.order_data).file()

            order_id = str(1000 + len(order_full_data) + 1)

            data_to_save = {
                "date_time": datetime.now().strftime("%d-%m-%Y %I:%M %p"),
                "order_id": order_id,
                "order": []
            }

            for index, order in enumerate(cls.order_data, start=1):
                data_to_save["order"].append({
                    str(index): {
                        "id": order.id,
                        "item_name": order.item_name,
                        "size_choice": order.size_choice,
                        "quantity": order.quantity
                    }
                })

            order_full_data.append(data_to_save)
            Createfile(PathModel.order_data).write_in_file(order_full_data)

        except Exception as e:
           Managingorders.order_logger.exception(
            f"UNEXPECTED ERROR IN Managingorder| Error: {e}")
           print("There is an issue. Please try again after some time.")
            
    @classmethod
    def new_order(cls):
        """
        Adds a new item to the current order."""
        try:
            check = Validationcheck()
            order = OrderModel()
            food_data = Createfile(PathModel.food_data).file()

            order_name = check.name_check( input("Enter name of the item you want: "), "Enter name of the item you want: ").title()

            
            item_found = False
            selected_item = None
            for meal in food_data:
                for _, categories in meal.items():
                    for category_name,items in categories.items():
                        for item in items:
                            if item["item_name"].lower() == order_name.lower():
                                selected_item = item
                                order.id=item["id"]
                                item_found = True
                                break
                        if item_found:
                            break
                    if item_found:
                        break
                if item_found:
                    break

            if not item_found:
                print("we did not have this item")
                return

            order.item_name = order_name
            order.quantity = check.quantity_chcek(input("Enter the quantity: "))
            print("\n")
            available_sizes = []
            for s in selected_item["size"]:
                print(f"- {s['name']} (₹{s['price']})")
                available_sizes.append(s["name"].lower())

            while True:
                size_choice = input("Enter size: ").title()
                if size_choice.lower() in available_sizes:
                    order.size_choice = size_choice
                    break
                else:
                    print("Invalid size. Please choose from available sizes.")
            found = False
            for existing_order in cls.order_data:
                if (
                    existing_order.item_name == order.item_name
                    and existing_order.size_choice == order.size_choice
                ):
                    existing_order.quantity = str(
                        int(existing_order.quantity) + int(order.quantity)
                    )
                    found = True
                    break

            if not found:
                cls.order_data.append(order)
        except Exception as e:
           Managingorders.order_logger.exception(
            f"UNEXPECTED ERROR IN Managingorder| Error: {e}")
           print("There is an issue. Please try again after some time.")

    @classmethod
    def show_all_order(cls):
        """
        Displays all current orders with calculated prices."""
        try:
            food_data = Createfile(PathModel.food_data).file()

            if len(cls.order_data) == 0:
                print("no order is there")
                return

            print("======Your Order=========")

            for order in cls.order_data:
                found = False
                for meal in food_data:
                    for _, categories in meal.items():
                        for _, items in categories.items():
                            for item in items:
                                if item["item_name"].lower() == order.item_name.lower():
                                    price = None
                                    for s in item["size"]:
                                        if s["name"].lower() == order.size_choice.lower():
                                            price = s["price"]
                                            break

                                    if price is not None:
                                        print(f"Item Name = {item['item_name']}")
                                        print(f"Size = {order.size_choice}")
                                        print(f"Price = {price}")
                                        print(f"Quantity = {order.quantity}")
                                        print("---------------------------")
                                        found = True
                                        break
                            if found:
                                break
                        if found:
                            break
                    if found:
                        break
        except Exception as e:
           Managingorders.order_logger.exception(
            f"UNEXPECTED ERROR IN Managingorder| Error: {e}")
           print("There is an issue. Please try again after some time.")

   


