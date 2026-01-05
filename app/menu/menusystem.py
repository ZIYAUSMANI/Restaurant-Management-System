from ..domain.billingsystem import Createfile
from ..model.models import PathModel, FoodItemModel
from ..validation.checkvalidation import Validationcheck
from .foodmenu import Managingfoodmenu
from ..logs.logger import get_logger



class Menumanagment:
    menu_logger = get_logger(PathModel.menu_log, "menusystem")
    """
    Handles complete menu management operations.

     Uses the following classes:
    - Createfile: Handles reading/writing JSON or file data.
    - Validetioncheck: Validates all user inputs like item name, price, quantity etc.
    - PathModel: Stores file paths for data storage .
    - FoodItemModel: Access food items model
    - Managingfoodmenu: Access show menu method.
    - logger: To handle unexpected errors 
    """
    @staticmethod
    def manage_menu():
        """ Displays the main menu management screen. """
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
        except Exception as e:
           Menumanagment.menu_logger.exception(
            f"UNEXPECTED ERROR IN manage_menu | Error: {e}")
           print("There is an issue. Please try again after some time.")

    @staticmethod
    def _choose_meal(action):
        """Allows the user to select a meal type."""
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
        except Exception as e:
           Menumanagment.menu_logger.exception(
            f"UNEXPECTED ERROR IN choose meal | Error: {e}")
           print("There is an issue. Please try again after some time.")


    @staticmethod
    def _choose_category(meal_data):
        """
        Displays available categories for the selected meal."""
        try:
            categories = list(meal_data.keys())

            while True:
                for i, cat in enumerate(categories, 1):
                    print(f"{i}. {cat}")
                print(f"{len(categories) + 1}. Back")

                try:
                    cat_choice = int(input("Enter category number = "))

                    if cat_choice == len(categories) + 1:
                        return None, None

                    if not 1 <= cat_choice <= len(categories):
                        print("Invalid choice!")
                        continue

                    category_name = categories[cat_choice - 1]
                    return category_name, meal_data[category_name]
                except ValueError:
                    print("Invalid input!")
        except Exception as e:
           Menumanagment.menu_logger.exception(
            f"UNEXPECTED ERROR IN choose category | Error: {e}")
           print("There is an issue. Please try again after some time.")



    @staticmethod
    def add_item(meal_type):
        """
        Adds a new food item to the selected meal and category."""
        try:
            food_menu = Createfile(PathModel.food_data).file()
            check = Validationcheck()

            for data in food_menu:
                if meal_type in data:
                    meal_data = data[meal_type]
                    break

            category_name, category_list = Menumanagment._choose_category(meal_data)
            if category_name is None:
                return

            item_name = check.name_check(input("Enter item name = "), "Enter item name = ").title()

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
                sizes.append({"name": "Half", "price": half})
                sizes.append({"name": "Full", "price": full})

            item.size = sizes

            category_list.append(item.__dict__)
            Menumanagment._reassign_ids(food_menu)
            Createfile(PathModel.food_data).write_in_file(food_menu)
            print(f"{item_name} added successfully!")

        except Exception as e:
           Menumanagment.menu_logger.exception(
            f"UNEXPECTED ERROR IN add_item in manage_menu | Error: {e}")
           print("There is an issue. Please try again after some time.")

            
    @staticmethod
    def delete_item(meal_type):
        """
        Deletes a food item from the selected meal and category."""
        try:
            food_menu = Createfile(PathModel.food_data).file()
            check = Validationcheck()

            for data in food_menu:
                if meal_type in data:
                    meal_data = data[meal_type]
                    break

            _,category_list = Menumanagment._choose_category(meal_data)
            if category_list is None:
                return

            item_name = check.name_check(input("Enter item name = "), "Enter item name = ").title()

            for item in category_list:
                if item["item_name"].lower() == item_name.lower():
                    category_list.remove(item)
                    Menumanagment._reassign_ids(food_menu)
                    Createfile(PathModel.food_data).write_in_file(food_menu)
                    print("Item deleted successfully!")
                    return

            print("Item not found!")

        except Exception as e:
           Menumanagment.menu_logger.exception(
            f"UNEXPECTED ERROR IN delete item inmanage_menu | Error: {e}")
           print("There is an issue. Please try again after some time.")

    @staticmethod
    def update_item(meal_type):
        """
        Updates an existing food item."""
        try:
            food_menu = Createfile(PathModel.food_data).file()
            check = Validationcheck()

            for data in food_menu:
                if meal_type in data:
                    meal_data = data[meal_type]
                    break

            category_name, category_list = Menumanagment._choose_category(meal_data)
            if category_name is None:
                return

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

        except Exception as e:
           Menumanagment.menu_logger.exception(
            f"UNEXPECTED ERROR IN update item in manage_menu | Error: {e}")
           print("There is an issue. Please try again after some time.")

    
    @staticmethod
    def _update_item_menu(item, category_name):
        """ Updates individual attributes of a food item."""
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

        except Exception as e:
           Menumanagment.menu_logger.exception(
            f"UNEXPECTED ERROR IN update item menu in manage_menu | Error: {e}")
           print("There is an issue. Please try again after some time.")

    @staticmethod
    def _reassign_ids(food_menu):
        """
        Reassigns sequential IDs to all food items."""
        try:
            new_id = 1
            for data in food_menu:
                for meal in ["BREAKFAST", "LUNCH", "DINNER"]:
                    if meal in data:
                        for cat_list in data[meal].values():
                            for item in cat_list:
                                item["id"] = str(new_id)
                                new_id += 1
        except Exception as e:
           Menumanagment.menu_logger.exception(
            f"UNEXPECTED ERROR IN manage_menu | Error: {e}")
           print("There is an issue. Please try again after some time.")
