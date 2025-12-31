from ..domain.billingsystem import Createfile
from ..model.models import PathModel, FoodItemModel
from ..validation.checkvalidation import Validationcheck
from .foodmenu import Managingfoodmenu

class Menumanagment:

    @staticmethod
    def manage_menu():
        while True:
            print("=========== Menu Management ===========")
            print("\n-------------------------------------")
            print("1. Show menu\n2. Add item\n3. Delete item\n4. Update item\n5. Back")
            print("\n-------------------------------------")
            try:
                choice = int(input("Enter your choice = "))
            except ValueError:
                print("Invalid input! Only numbers are allowed.")
                continue

            if choice == 1:
                Managingfoodmenu.show_food_menu()
            elif choice == 2:
                Menumanagment._choose_meal("add")
            elif choice == 3:
                Menumanagment._choose_meal("delete")
            elif choice == 4:
                Menumanagment._choose_meal("update")
            elif choice == 5:
                break
            else:
                print("Invalid choice! Please select between 1 to 5.")

    @staticmethod
    def _choose_meal(action):
        while True:
            print(f"=========== {action.title()} item in menu ===========")
            print("1. Breakfast\n2. Lunch\n3. Dinner\n4. Back")
            try:
                choice = int(input("Enter your choice = "))
            except ValueError:
                print("Invalid input! Only numbers are allowed.")
                continue

            meal_map = {1: "BREAKFAST", 2: "LUNCH", 3: "DINNER"}
            if choice in meal_map:
                meal_type = meal_map[choice]
                if action == "add":
                    Menumanagment.add_item(meal_type)
                elif action == "delete":
                    Menumanagment.delete_item(meal_type)
                elif action == "update":
                    Menumanagment.update_item(meal_type)
            elif choice == 4:
                break
            else:
                print("Invalid choice! Please select between 1 to 4.")

    @staticmethod
    def dict_to_model(data):
        obj = FoodItemModel()
        obj.id = data.get("id")
        obj.item_name = data.get("item_name")
        obj.category = data.get("category")
        obj.price = data.get("price")
        return obj

    @staticmethod
    def model_to_dict(obj):
        return {
            "id": obj.id,
            "item_name": obj.item_name,
            "category": obj.category,
            "price": obj.price
        }

    @staticmethod
    def add_item(meal_type):
        food_menu = Createfile(PathModel.food_data).file()
        check = Validationcheck()

        for data in food_menu:
            if meal_type in data:
                menu_list = data[meal_type]
                break

        name = check.name_check(input("Enter item name = ")).title()

        for item in menu_list:
            model = Menumanagment.dict_to_model(item)
            if model.item_name.lower() == name.lower():
                print("Item already exists!")
                return

        model = FoodItemModel()
        model.id = "0"
        model.item_name = name
        model.category = check.category_check(input("Enter category = "))
        model.price = check.price_check(input("Enter price = "))

        while True:
            try:
                position = int(input(f"Enter position to insert (1 to {len(menu_list)+1}) = "))
                if 1 <= position <= len(menu_list)+1:
                    break
                print("Invalid position!")
            except ValueError:
                print("Enter a valid number!")

        menu_list.insert(position-1, Menumanagment.model_to_dict(model))

        new_id = 1
        for data in food_menu:
            for meal in ["BREAKFAST", "LUNCH", "DINNER"]:
                for item in data[meal]:
                    item["id"] = str(new_id)
                    new_id += 1

        Createfile(PathModel.food_data).write_in_file(food_menu)
        print("Item added successfully!")

    @staticmethod
    def delete_item(meal_type):
        food_menu = Createfile(PathModel.food_data).file()
        check = Validationcheck()

        for data in food_menu:
            if meal_type in data:
                menu_list = data[meal_type]
                break

        name = check.name_check(input("Enter item name = ")).title()

        for item in menu_list:
            model = Menumanagment.dict_to_model(item)
            if model.item_name == name:
                menu_list.remove(item)

                new_id = 1
                for data in food_menu:
                    for meal in ["BREAKFAST", "LUNCH", "DINNER"]:
                        for i in data[meal]:
                            i["id"] = str(new_id)
                            new_id += 1

                Createfile(PathModel.food_data).write_in_file(food_menu)
                print("Item deleted successfully!")
                return

        print("Item not found!")

    @staticmethod
    def update_food_menu(menu_item_dict, food_menu):
        check = Validationcheck()
        model = Menumanagment.dict_to_model(menu_item_dict)

        while True:
            print("\n=========== Update item detail ==========")
            print("\n-----------------------------------------")
            print("1. Name\n2. Category\n3. Price\n4. Back")
            print("\n-----------------------------------------")
            try:
                choice = int(input("Enter your choice = "))
            except ValueError:
                print("Invalid input!")
                continue

            if choice == 1:
                model.item_name = check.name_check(input("Enter name = ")).title()
            elif choice == 2:
                model.category = check.category_check(input("Enter category = "))
            elif choice == 3:
                model.price = check.price_check(input("Enter price = "))
            elif choice == 4:
                menu_item_dict.update(Menumanagment.model_to_dict(model))
                Createfile(PathModel.food_data).write_in_file(food_menu)
                print("Item updated successfully!")
                break
            else:
                print("Invalid choice! Please select between 1 to 4.")

    @staticmethod
    def update_item(meal_type):
        food_menu = Createfile(PathModel.food_data).file()
        check = Validationcheck()

        for data in food_menu:
            if meal_type in data:
                menu_list = data[meal_type]
                break

        name = check.name_check(input("Enter item name = ")).title()

        for item in menu_list:
            model = Menumanagment.dict_to_model(item)
            if model.item_name == name:
                Menumanagment.update_food_menu(item, food_menu)
                return

        print("Item not found!")
