from ..domain.billingsystem import Createfile
from ..model.models import PathModel, FoodItemModel
from ..validation.checkvalidation import Validationcheck
from .foodmenu import Managingfoodmenu
from ..logs.logger import logger


class Menumanagment:

    @staticmethod
    def manage_menu():
        try:
            while True:
                print("=========== Menu Management ===========")
                print("1. Show menu\n2. Add item\n3. Delete item\n4. Update item\n5. Back")

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
        except Exception:
            logger.exception("Unhandled error in manage_menu")
            print("Something went wrong! Please contact admin.")

    @staticmethod
    def _choose_meal(action):
        try:
            while True:
                print(f"\n=========== {action.title()} item ===========")
                print("1. Breakfast\n2. Lunch\n3. Dinner\n4. Back")

                try:
                    choice = int(input("Enter your choice = "))
                except ValueError:
                    print("Invalid input!")
                    continue

                meal_map = {1: "BREAKFAST", 2: "LUNCH", 3: "DINNER"}

                if choice in meal_map:
                    if action == "add":
                        Menumanagment.add_item(meal_map[choice])
                    elif action == "delete":
                        Menumanagment.delete_item(meal_map[choice])
                    elif action == "update":
                        Menumanagment.update_item(meal_map[choice])
                elif choice == 4:
                    break
                else:
                    print("Invalid choice!")
        except Exception:
            logger.exception("Unhandled error in _choose_meal")
            print("Unexpected error occurred!")

    @staticmethod
    def add_item(meal_type):
        try:
            food_menu = Createfile(PathModel.food_data).file()
            check = Validationcheck()

            for data in food_menu:
                if meal_type in data:
                    meal_data = data[meal_type]
                    break

            categories = list(meal_data.keys())

            while True:
                for i, cat in enumerate(categories, 1):
                    print(f"{i}. {cat}")
                try:
                    cat_choice = int(input("Enter category number = "))
                    if not 1 <= cat_choice <= len(categories):
                        print("Invalid choice! Select a valid category.")
                        continue
                    category_name = categories[cat_choice - 1]
                    break
                except ValueError:
                    print("Invalid input! Only numbers are allowed.")

            category_list = meal_data[category_name]

            item_name = check.name_check(
                input("Enter item name = "), "Enter item name = "
            ).title()

            for item in category_list:
                if item["item_name"].lower() == item_name.lower():
                    print("Item already exists!")
                    return

            item = FoodItemModel()
            item.id = "0"
            item.item_name = item_name

            sizes = []

            if category_name.lower() == "roti":
                single = check.price_check(
                    input("Enter Single price = "), "Enter Single price = "
                )
                double = check.price_check(
                    input("Enter Double price = "), "Enter Double price = "
                )
                sizes.append({"name": "Single", "price": single})
                sizes.append({"name": "Double", "price": double})
            else:
                half = check.price_check(
                    input("Enter Half price = "), "Enter Half price = "
                )
                full = check.price_check(
                    input("Enter Full price = "), "Enter Full price = "
                )
                sizes.append({"name": "Half Plate", "price": half})
                sizes.append({"name": "Full Plate", "price": full})

            item.size = sizes

            category_list.append(item.__dict__)
            Menumanagment._reassign_ids(food_menu)
            Createfile(PathModel.food_data).write_in_file(food_menu)
            print(f"{item_name} added successfully!")

        except Exception:
            logger.exception("Unhandled error in add_item")
            print("Failed to add item!")
            
    @staticmethod
    def delete_item(meal_type):
        try:
            food_menu = Createfile(PathModel.food_data).file()
            check = Validationcheck()

            for data in food_menu:
                if meal_type in data:
                    meal_data = data[meal_type]
                    break

            categories = list(meal_data.keys())

            while True:
                for i, cat in enumerate(categories, 1):
                    print(f"{i}. {cat}")
                try:
                    cat_choice = int(input("Enter category number = "))
                    if not 1 <= cat_choice <= len(categories):
                        print("Invalid choice!")
                        continue
                    category_name = categories[cat_choice - 1]
                    break
                except ValueError:
                    print("Invalid input!")

            category_list = meal_data[category_name]

            item_name = check.name_check(
                input("Enter item name = "), "Enter item name = "
            ).title()

            for item in category_list:
                if item["item_name"].lower() == item_name.lower():
                    category_list.remove(item)
                    Menumanagment._reassign_ids(food_menu)
                    Createfile(PathModel.food_data).write_in_file(food_menu)
                    print("Item deleted successfully!")
                    return

            print("Item not found!")

        except Exception:
            logger.exception("Unhandled error in delete_item")
            print("Delete failed!")

    @staticmethod
    def update_item(meal_type):
        try:
            food_menu = Createfile(PathModel.food_data).file()
            check = Validationcheck()

            for data in food_menu:
                if meal_type in data:
                    meal_data = data[meal_type]
                    break

            categories = list(meal_data.keys())

            while True:
                for i, cat in enumerate(categories, 1):
                    print(f"{i}. {cat}")
                try:
                    cat_choice = int(input("Enter category number = "))
                    if not 1 <= cat_choice <= len(categories):
                        print("Invalid choice!")
                        continue
                    category_name = categories[cat_choice - 1]
                    break
                except ValueError:
                    print("Invalid input!")

            category_list = meal_data[category_name]

            item_name = check.name_check(
                input("Enter item name = "), "Enter item name = "
            ).title()

            for item in category_list:
                if item["item_name"].lower() == item_name.lower():
                    Menumanagment._update_item_menu(item, category_name)
                    Createfile(PathModel.food_data).write_in_file(food_menu)
                    print("Item updated successfully!")
                    return

            print("Item not found!")

        except Exception:
            logger.exception("Unhandled error in update_item")
            print("Update failed!")

    
    @staticmethod
    def _update_item_menu(item, category_name):
        try:
            check = Validationcheck()

            while True:
                print("\nWhat do you want to update?")
                print("1. Name")
                if category_name.lower() == "roti":
                    print("2. Single price")
                    print("3. Double price")
                else:
                    print("2. Half price")
                    print("3. Full price")
                print("4. Back")

                try:
                    choice = int(input("Enter your choice = "))
                except ValueError:
                    print("Invalid input!")
                    continue

                if choice == 1:
                    item["item_name"] = check.name_check(
                        input("Enter new name = "), "Enter new name = "
                    ).title()
                elif choice == 2:
                    item["size"][0]["price"] = check.price_check(
                        input("Enter new price = "), "Enter new price = "
                    )
                elif choice == 3:
                    item["size"][1]["price"] = check.price_check(
                        input("Enter new price = "), "Enter new price = "
                    )
                elif choice == 4:
                    break
                else:
                    print("Invalid choice!")

        except Exception:
            logger.exception("Unhandled error in _update_item_menu")
            print("Update failed!")

    @staticmethod
    def _reassign_ids(food_menu):
        try:
            new_id = 1
            for data in food_menu:
                for meal in ["BREAKFAST", "LUNCH", "DINNER"]:
                    if meal in data:
                        for cat_list in data[meal].values():
                            for item in cat_list:
                                item["id"] = str(new_id)
                                new_id += 1
        except Exception:
            logger.exception("Unhandled error in _reassign_ids")
