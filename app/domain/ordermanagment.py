from ..validation.checkvalidation import Validationcheck
from ..model.models import OrderModel
from ..domain.filehandler import Createfile
from ..model.models import PathModel
from ..menu.foodmenu import Managingfoodmenu
from .billingsystem import Generatesbill

class Managingorders:
    current_booking = None
    order_data = []
    @staticmethod
    def order_menu():
        while True:
            print("\n" + "="*35)
            print("           ORDER MENU")
            print("="*35)
            print("1. Show Food Menu")
            print("2. Add Order")
            print("3. Update Order")
            print("4. Delete Order")
            print("5. Show All Orders")
            print("6. Generate Bill")
            print("="*35)

            try:
                choice = int(input("Enter your choice (1-6): "))
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
                print("\n--- Update Order ---")
                Managingorders.update_order()
            elif choice == 4:
                print("\n--- Delete Order ---")
                Managingorders.delete_order()
            elif choice == 5:
                print("\n--- All Orders ---")
                Managingorders.show_all_order()
            elif choice == 6:
                order_obj = Managingorders()
                bill = Generatesbill(order_obj,Managingorders.current_booking)
                bill.show_bill()
                break
            else:
                print("Invalid choice! Please select a number between 1 and 6.")


    def update_order_menu(self, order):
        check=Validationcheck()
        while True:
            print("\n========= Update Your Order ========")
            print("\n------------------------------------")
            print("1.id\n2.quantity\n3.back")
            print("\n------------------------------------")

            try:
                choice = int(input("Enter your choice = "))
            except ValueError:
                print("Invalid input! Only numbers are allowed.")
                continue

            if choice == 1:
                order.id = check.id_chcek(input("enter id of the item you want: "))
            elif choice == 2:
                order.quantity = check.quantity_chcek(input("enter the quantity: "))
            elif choice == 3:
                break
            else:
                print("Invalid choice! Please select between 1 to 3.")

    @classmethod
    def new_order(cls):
        check = Validationcheck()
        found = False

        order = OrderModel()
        order.id = check.id_chcek(input("enter id of the item you want: "))
        order.quantity = check.quantity_chcek(input("enter the quantity: "))

        for order_item in cls.order_data:
            if order_item.id == order.id:
                order_item.quantity = str(
                    int(order_item.quantity) + int(order.quantity)
                )
                found = True
                break

        if found is False:
            cls.order_data.append(order)

    @classmethod
    def update_order(cls):
        check=Validationcheck()
        if len(cls.order_data) == 0:
            print("no order is there")
        else:
            id =check.id_chcek(input("enter id of the item you want: "))
            found = False

            for order in cls.order_data:
                if order.id == id:
                    cls().update_order_menu(order)
                    found = True
                    break

            if found is False:
                print("there no item order with this id!")


    @classmethod
    def delete_order(cls):
        check = Validationcheck()
        if len(cls.order_data) == 0:
            print("no order is there")
        else:
            id = check.id_chcek(input("enter id of the item you want: "))
            found = False

            for order in cls.order_data:
                if order.id == id:
                    cls.order_data.remove(order)
                    found = True
                    print("order item cancel successfully!")
                    break

            if found is False:
                print("there no item order with this id!")

    @classmethod
    def show_all_order(cls):
        order_data=OrderModel()
        food_data=Createfile(PathModel.food_data)
        order_data.foodmenu=food_data.file()
        if len(cls.order_data) == 0:
            print("no order is there")
        else:
            print("======Your Order=========")
            for order in cls.order_data:
                order_data.id = order.id

                for food in order_data.foodmenu:
                    for k, v in food.items():
                        for item in v:
                            if item["id"] == order_data.id:
                                for key, value in item.items():
                                    print(f"{key} = {value}")

                print(f"quantity = {order.quantity}")
                print("---------------------------")
