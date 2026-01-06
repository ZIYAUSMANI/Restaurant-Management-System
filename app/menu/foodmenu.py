from ..domain.filehandler import Createfile
from ..model.models import PathModel
from ..model.models import FoodItemModel
from ..model.models import FoodCategoryModel
from ..logs.logger import get_logger

class Managingfoodmenu:
    menu_logger = get_logger(PathModel.menu_log, "foodmenu")
    """
    Handles complete show food menu operations.

     Uses the following classes:
    - Createfile: Handles reading/writing JSON or file data.
    - PathModel: Stores file paths for data storage .
    - FoodItemModel: Access food items model
    - FoodCategoryModel: Access food category model.
    - logger: To handle unexpected errors 
    """
    categories = []
    @classmethod
    def convert_food_data_to_model(cls, food_data):
        """
            convert food data to model the use in show menu method"""


        cls.categories = []

        for meal_dict in food_data:
            for meal_name, categories_dict in meal_dict.items():
                for cat_name, items_list in categories_dict.items():

                    category = FoodCategoryModel()
                    category.meal_name = meal_name
                    category.category_name = cat_name
                    category.items = []

                    for item in items_list:
                        food = FoodItemModel()
                        food.id = item["id"]
                        food.item_name = item["item_name"]

                        
                        food.half_price = "-"
                        food.full_price = "-"

                        for size in item.get("size", []):
                            size_name = size["name"].lower()
                            price = size["price"]

                            if "half" in size_name or "single" in size_name:
                                    food.half_price = price
                            elif "full" in size_name or "double" in size_name:
                                    food.full_price = price
                        category.items.append(food)

                    cls.categories.append(category)

        return cls.categories

    @staticmethod
    def show_food_menu():
        """ show food menu operations."""

        try:
            ob = Createfile(PathModel.food_data)
            food_data = ob.file()
            Managingfoodmenu.convert_food_data_to_model(food_data)

            print("|------------------------------------------------------------|")
            print("|======================== FOOD MENU =========================|")
            print("|------------------------------------------------------------|")

            last_meal = None

            for category in Managingfoodmenu.categories:

                if category.meal_name != last_meal:
                    print(f"\n|{'='*((60 - len(category.meal_name) - 2)//2)} {category.meal_name.upper()} {'='*((60 - len(category.meal_name) - 2)//2 + (60 - len(category.meal_name) - 2)%2)}|")
                    print("|------------------------------------------------------------|")
                    last_meal = category.meal_name
                print("|                                                            |")
                print(f"|>>> {category.category_name:<56}|")
                print("|                                                            |")
                print("|------------------------------------------------------------|")
                        
                print(
                    f"|{'ID':<5}"
                    f"{'Item Name':<16}"
                    f"{'Half/Single Price':<21}"
                    f"{'Full/Double Price':<16} |"
                )

                print("|------------------------------------------------------------|")

                for food in category.items:
                    print(
                        f"|{food.id:<5}{food.item_name:<23}"
                        f"{str(food.half_price) + ' ₹':<17}{str(food.full_price) + ' ₹':<14} |"
                    )

                print("|------------------------------------------------------------|")

            
        except Exception as e:
            Managingfoodmenu.menu_logger.exception(
                f"UNEXPECTED ERROR in show_food_menu | Error: {e}"
            )
            print("Unable to display menu. Please try again later.")
