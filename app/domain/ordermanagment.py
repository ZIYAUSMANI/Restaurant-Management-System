from .filehandler import Createfile
from ..model.models import PathModel, OrderModel
from datetime import datetime, timedelta
from ..validation.checkvalidation import Validationcheck
from ..logs.logger import get_logger


class Ordermanaingsystem:

    @staticmethod
    def dict_to_order_model(data):
        try:
            order = OrderModel()
            order.id = data.get("id")
            order.item_name = data.get("item_name")
            order.quantity = data.get("quantity")
            order.size_choice = data.get("size_choice")
            return order
        except Exception as e:
            get_logger.error(f"Error in dict_to_order_model: {e}")

    @staticmethod
    def order_model_to_dict(order):
        try:
            return order.__dict__
        except Exception as e:
            get_logger.error(f"Error in order_model_to_dict: {e}")

    @staticmethod
    def remove_expired_order():
        try:
            order_data = Createfile(PathModel.order_data).file()
            current_time = datetime.now()
            updated_orders = []

            for data in order_data:
                order_time = datetime.strptime(
                    data["date_time"], "%d-%m-%Y %I:%M %p"
                )
                if current_time - order_time <= timedelta(hours=2):
                    updated_orders.append(data)

            Createfile(PathModel.order_data).write_in_file(updated_orders)
        except Exception as e:
            get_logger.error(f"Error in remove_expired_order: {e}")

    @staticmethod
    def show_all_order_save():
        try:
            Ordermanaingsystem.remove_expired_order()
            order_data = Createfile(PathModel.order_data).file()

            if len(order_data) == 0:
                print("no order taken")
            else:
                for data in order_data:
                    print(f"date time = {data['date_time']}")
                    print(f"order id = {data['order_id']}")

                    for order_take in data["order"]:
                        for _, value in order_take.items():
                            print(
                                f"ID: {value['id']} | "
                                f"Item: {value['item_name']} | "
                                f"Size: {value['size_choice']} | "
                                f"Quantity: {value['quantity']}"
                            )
                    print("-" * 68)
        except Exception as e:
            get_logger.error(f"Error in show_all_order_save: {e}")

    @staticmethod
    def delete_order():
        try:
            Ordermanaingsystem.remove_expired_order()
            check = Validationcheck()
            order_data = Createfile(PathModel.order_data).file()

            if len(order_data) == 0:
                print("No order is there")
                return

            enter_order_id = check.get_valid_order_id(
                input("Enter ID of the order you want to delete: ").strip()
            )

            for order in order_data:
                if order["order_id"] == enter_order_id:

                    if len(order["order"]) == 1:
                        order_data.remove(order)
                        print("Only one item found. Full order deleted successfully.")
                        Createfile(PathModel.order_data).write_in_file(order_data)
                        return

                    while True:
                        print("\n1. Delete full order")
                        print("2. Delete item from the order")
                        print("3. Back")

                        try:
                            choice = int(input("Enter your choice (1-3): "))
                        except ValueError:
                            print("Invalid input! Please enter a number only.")
                            continue

                        if choice == 1:
                            order_data.remove(order)
                            print("Full order deleted successfully.")
                            break

                        elif choice == 2:
                            item_name = check.name_check(
                                input("Enter item you want to delete: "),
                                "Enter item you want to delete: "
                            ).title()

                            for item in order["order"]:
                                for _, value in item.items():
                                    if value["item_name"].lower() == item_name.lower():
                                        order["order"].remove(item)
                                        print(f"Item '{item_name}' deleted successfully.")
                                        Createfile(PathModel.order_data).write_in_file(order_data)
                                        return

                            print(f"This item '{item_name}' is not in this order.")
                            break

                        elif choice == 3:
                            break

                    Createfile(PathModel.order_data).write_in_file(order_data)
                    return

            print(f"There is no order with ID '{enter_order_id}'.")
        except Exception as e:
            get_logger.error(f"Error in delete_order: {e}")

    @classmethod
    def upadate_order(cls):
        try:
            Ordermanaingsystem.remove_expired_order()
            check = Validationcheck()
            order_data = Createfile(PathModel.order_data).file()

            if len(order_data) == 0:
                print("No order is there")
                return

            enter_order_id = check.get_valid_order_id(
                input("Enter ID of the order you want to update: ").strip()
            )

            for order in order_data:
                if order["order_id"] == enter_order_id:
                    order_items = order["order"]
                    break
            else:
                print(f"There is no order with ID '{enter_order_id}'.")
                return

            item_name = check.name_check(
                input("Enter item you want to update: "),
                "Enter item you want to update: "
            ).title()

            for single_order in order_items:
                for _, value in single_order.items():
                    if value["item_name"].lower() == item_name.lower():
                        order_model = cls.dict_to_order_model(value)
                        cls.update_order_menu(order_model)
                        value.update(cls.order_model_to_dict(order_model))
                        Createfile(PathModel.order_data).write_in_file(order_data)
                        return

            print("no item order with this item name")
        except Exception as e:
            get_logger.error(f"Error in upadate_order: {e}")

    @staticmethod
    def update_order_menu(order):
        try:
            check = Validationcheck()
            food_data = Createfile(PathModel.food_data).file()
            item_category = None

            for meal in food_data:
                for _, categories in meal.items():
                    for cat_name, items in categories.items():
                        for item in items:
                            if item["item_name"].lower().startswith(order.item_name.lower()):
                                item_category = cat_name.lower()
                                break
                        if item_category:
                            break
                    if item_category:
                        break
                if item_category:
                    break

            while True:
                print("\n========= Update Your Order ========")
                print("1. Size")
                print("2. Quantity")
                print("3. Back")

                try:
                    choice = int(input("Enter your choice = "))
                except ValueError:
                    print("Invalid input! Only numbers are allowed.")
                    continue

                if choice == 1:
                    order.size_choice = check.size_check(
                        input(f"Enter new size (current: {order.size_choice}): ").title().strip(),
                        item_category
                    )
                    print(f"Size updated to {order.size_choice}")

                elif choice == 2:
                    order.quantity = check.quantity_chcek(
                        input(f"Enter new quantity (current: {order.quantity}): ")
                    )
                    print(f"Quantity updated to {order.quantity}")

                elif choice == 3:
                    break
        except Exception as e:
            get_logger.error(f"Error in update_order_menu: {e}")

    @staticmethod
    def order_managment():
        try:
            while True:
                print("\n" + "=" * 35)
                print("           ORDER MENU")
                print("=" * 35)
                print("1. Show all Orders")
                print("2. delete Order")
                print("3. update Order")
                print("4. back")
                print("=" * 35)

                try:
                    choice = int(input("Enter your choice (1-4): "))
                except ValueError:
                    print("Invalid input! Please enter a number only.")
                    continue

                if choice == 1:
                    print("\n--- Show All Order Save---")
                    Ordermanaingsystem.show_all_order_save()

                elif choice == 2:
                    print("\n--- Delete Order ---")
                    Ordermanaingsystem.delete_order()

                elif choice == 3:
                    print("\n--- Update Order ---")
                    Ordermanaingsystem.upadate_order()

                elif choice == 4:
                    break

                else:
                    print("Invalid choice! Please select a number between 1 and 4.")

        except Exception as e:
            get_logger.error(f"Error in order_managment: {e}")
