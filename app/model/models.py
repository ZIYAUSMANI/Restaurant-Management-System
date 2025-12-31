class UserModel:
    id = None
    name = None
    email = None
    password = None
    address = None
    department = None
    past_experience = None
    role = None

class PathModel:
    registration_data=r"C:\indixpert\python_project\app\database\userdata.json" 
    food_data= r"C:\indixpert\python_project\app\database\fooddata.json" 
    table_data=r"C:\indixpert\python_project\app\database\tabledata.json" 
    table_booked=r"C:\indixpert\python_project\app\database\tablebooking.json"
    bill_data=r"C:\indixpert\python_project\app\database\billdata.json"
    order_data=r"C:\indixpert\python_project\app\database\orderdata.json"
    log_data=r"C:\indixpert\python_project\app\logs\logdata.text"

class FoodItemModel: 
    id = None
    item_name = None
    category = None
    price = None

class FoodCategoryModel:
    category_name = None
    items = None

class OrderModel:
    id = None
    quantity = None
    foodmenu=None

class BillItemModel:
    id = None
    item_name = None
    quantity = None
    price = None
    total = None
    seats=None

class BookingModel:
    booking_id = None
    date = None
    time_slot = None
    table_no = None
    seats_booked = None
    created_at = None

class TableModel:
    table_no = None
    total_seats = None