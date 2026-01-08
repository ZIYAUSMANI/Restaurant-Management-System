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
                    Menumanagment._choose_meal()   

                elif choice == 3:
                    Menumanagment.delete_item()   

                elif choice == 4:
                    Menumanagment.update_item()

                elif choice == 5:
                    break

                else:
                    print("Invalid choice! Please select between 1 to 5.")

        except Exception as e:
            Menumanagment.menu_logger.exception(
                f"UNEXPECTED ERROR IN manage_menu | Error: {e}")
            print("There is an issue. Please try again after some time.")

    @staticmethod
    def _choose_meal():
        """Allows the user to select a meal type for adding item."""
        try:
            while True:
                print("\n=========== Add Item ===========")
                print("1. Breakfast\n2. Lunch\n3. Dinner\n4. Back")

                try:
                    choice = int(input("Enter your choice = "))
                except ValueError:
                    print("Invalid input!")
                    continue

                meal_map = {
                    1: "BREAKFAST",
                    2: "LUNCH",
                    3: "DINNER"
                }

                if choice in meal_map:
                    Menumanagment.add_item(meal_map[choice])

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

            print("\nChoose price type to add:")
            print("1. Half / Full")
            print("2. Single / Double")
            while True:
                choice = input("Enter 1 or 2 = ").strip()
                if choice in ["1", "2"]:
                    break
                print("Invalid input! Enter 1 or 2.")

            sizes = []
            if choice == "1":
                half = check.price_check(input("Enter Half price = "), "Enter Half price = ")
                full = check.price_check(input("Enter Full price = "), "Enter Full price = ")
                sizes.append({"name": "Half", "price": half})
                sizes.append({"name": "Full", "price": full})
            else:
                single = check.price_check(input("Enter Single price = "), "Enter Single price = ")
                double = check.price_check(input("Enter Double price = "), "Enter Double price = ")
                sizes.append({"name": "Single", "price": single})
                sizes.append({"name": "Double", "price": double})

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
    def delete_item():
        """Deletes a food item by name without asking for meal or category."""
        try:
            food_menu = Createfile(PathModel.food_data).file()
            check = Validationcheck()

            item_name = check.name_check(input("Enter the name of the item to delete = "), "Enter item name = ").title()

            for data in food_menu:
                for categories in data.values(): 
                    for cat_list in categories.values():  
                        for item in cat_list:
                            if item["item_name"].lower() == item_name.lower():
                                cat_list.remove(item)
                                Menumanagment._reassign_ids(food_menu)
                                Createfile(PathModel.food_data).write_in_file(food_menu)
                                print(f"{item_name} deleted successfully!")
                                return

            print("Item not found!")

        except Exception as e:
            Menumanagment.menu_logger.exception(
                f"UNEXPECTED ERROR IN delete_item | Error: {e}")
            print("There is an issue. Please try again after some time.")


    @staticmethod
    def update_item():
        """Updates a food item by name without asking for meal or category."""
        try:
            food_menu = Createfile(PathModel.food_data).file()
            check = Validationcheck()

            item_name = check.name_check(input("Enter the name of the item to update = "), "Enter item name = ").title()

            for data in food_menu:
                for categories in data.values(): 
                    for cat_list in categories.values():  
                        for item in cat_list:
                            if item["item_name"].lower() == item_name.lower():
                                Menumanagment._update_item_menu(item)
                                Createfile(PathModel.food_data).write_in_file(food_menu)
                                return

            print("Item not found!")

        except Exception as e:
            Menumanagment.menu_logger.exception(
                f"UNEXPECTED ERROR IN update_item | Error: {e}")
            print("There is an issue. Please try again after some time.")

    @staticmethod
    def _update_item_menu(item):
        """Updates individual attributes of a food item based on actual stored sizes."""
        try:
            check = Validationcheck()

            while True:
                print("\nWhat do you want to update?")
                print("1. Name")

                price_options = [s["name"] for s in item["size"]]
                for idx, name in enumerate(price_options, 2):
                    print(f"{idx}. {name} price")
                print(f"{len(price_options) + 2}. Back")

                try:
                    choice = int(input("Enter your choice = "))
                except ValueError:
                    print("Invalid input!")
                    continue

                if choice == 1:
                    item["item_name"] = check.name_check(
                        input("Enter new name = "), "Enter new name = ").title()
                    print("item name update successfully!")
                    
                elif 2 <= choice <= len(price_options) + 1:
                    price_index = choice - 2
                    price_name = price_options[price_index]
                    item["size"][price_index]["price"] = check.price_check(
                        input(f"Enter new {price_name} price = "), f"Enter new {price_name} price = "
                    )
                    print("item_name price update successfully!")
                elif choice == len(price_options) + 2:
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
