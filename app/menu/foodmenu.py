from ..domain.filehandler import Createfile
from ..model.models import PathModel
from ..model.models import FoodItemModel
from ..model.models import FoodCategoryModel


class Managingfoodmenu:
    categories = []

    @classmethod
    def convert_food_data_to_model(cls, food_data):
        cls.categories = []

        for meal_dict in food_data:
            for meal_name, categories_dict in meal_dict.items():
                for cat_name, items_list in categories_dict.items():
                    category = FoodCategoryModel()
                    category.category_name = cat_name
                    category.items = []

                    for item in items_list:
                        food = FoodItemModel()
                        food.id = item["id"]
                        food.item_name = item["item_name"]
                        food.category = cat_name

                        if "size" in item:
                            food.size = item["size"]
                        elif "price" in item:
                            food.size = [{"name": "Full Plate", "price": item["price"]}]
                        else:
                            food.size = [{"name": "Full Plate", "price": 0}]

                        category.items.append(food)

                    cls.categories.append(category)

        return cls.categories

    @staticmethod
    def show_food_menu():
        ob = Createfile(PathModel.food_data)
        food_data = ob.file()
        Managingfoodmenu.convert_food_data_to_model(food_data)

        print("|------------------------------------------------------------|")
        print("|======================== FOOD MENU =========================|")
        print("|------------------------------------------------------------|")

        for category in Managingfoodmenu.categories:
            print(f"\n|  {category.category_name:<50}|")
            print("|------------------------------------------------------------|")
            print(f"|{'ID':<5}{'Item Name':<30}{'Half Price':<12}{'Full Price':<12}|")
            print("|------------------------------------------------------------|")

            for food in category.items:
                half_price = ""
                full_price = ""
                for s in food.size:
                    if s["name"].lower() == "half plate":
                        half_price = f"{s['price']} ₹"
                    elif s["name"].lower() == "full plate":
                        full_price = f"{s['price']} ₹"
                    else:
                        full_price = f"{s['price']} ₹"

                print(f"|{food.id:<5}{food.item_name:<30}{half_price:<12}{full_price:<12}|")
            print("|------------------------------------------------------------|")
