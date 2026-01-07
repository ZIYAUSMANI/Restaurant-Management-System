class UserModel:
    id = None
    name = None
    email = None
    password = None
    address = None
    department = None
    past_experience = None
    role = None
    
class DefaultModel:
    admin = "admin"
    staff = "staff"

class PathModel:
    registration_data=r"C:\indixpert\python_project\app\database\userdata.json" 
    food_data= r"C:\indixpert\python_project\app\database\fooddata.json" 
    table_data=r"C:\indixpert\python_project\app\database\tabledata.json" 
    table_booked=r"C:\indixpert\python_project\app\database\tablebooking.json"
    bill_data=r"C:\indixpert\python_project\app\database\billdata.json"
    order_data=r"C:\indixpert\python_project\app\database\orderdata.json"
    inventory_data=r"C:\indixpert\python_project\app\database\Food_Inventory.json"
    athu_log=r"C:\indixpert\python_project\app\logs\logs_of_authentication.text"
    menu_log=r"C:\indixpert\python_project\app\logs\logs_foodmenu.text"
    order_log=r"C:\indixpert\python_project\app\logs\logs_order.text"
    table_log =r"C:\indixpert\python_project\app\logs\logs_tablebooking.text"
    staff_menu_logs=r"C:\indixpert\python_project\app\logs\logs_staffmenu.text"
    bill_logs=r"C:\indixpert\python_project\app\logs\logs_billing.text"
    report_logs=r"C:\indixpert\python_project\app\logs\logs_report.text"
    admin_menu_logs=r"C:\indixpert\python_project\app\logs\logs_adminmenu.text"
    inventory_logs=r"C:\indixpert\python_project\app\logs\logs_inventory.text"
    furniture_inventory_data=r"C:\indixpert\python_project\app\database\ furniture_inventory_data.json"

class FoodItemModel:
    id = None
    item_name = None
    half_price = None
    full_price = None

class FoodCategoryModel:
    meal_name=None 
    category_name = None
    items = None

class OrderModel:
    id = None
    item_name = None
    quantity = None
    size_choice = None
    
    
class BillItemModel:
    id = None
    item_name = None
    quantity = None
    price = None
    total = None
    seats=None
    items = None  
    tables = None

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

class InventoryItemModel:
    name = None
    quantity = None
    unit = None
    reorder_level = None
    purchase_date = None
    expiry_date = None

class FurnitureItemModel:
    name = None
    quantity = None
    material = None
    reorder_level = None
    purchase_date = None
    warranty_end = None
