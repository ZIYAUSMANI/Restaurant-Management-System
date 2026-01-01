import re
import msvcrt
from ..domain.filehandler import Createfile
from ..model.models import PathModel

class Validationcheck:
    def name_check(self, value,prompt):
        while True:
            stripped_value = value.strip()

            if not (3 <= len(stripped_value) <= 20):
                print("Invalid name! Length must be between 3 and 20 characters.")
                value = input(prompt)
                continue

            if stripped_value.count(" ") > 2:
                print("Invalid name! Only up to 2 spaces are allowed.")
                value = input(prompt)
                continue

            if not stripped_value.replace(" ", "").isalpha():
                print("Invalid name! Name should contain only letters.")
                value = input(prompt)
                continue

            letters_only = stripped_value.replace(" ", "").lower()
            if len(set(letters_only)) == 1:
                print("Invalid name! Name cannot contain the same letter repeatedly.")
                value = input(prompt)
                continue

            return stripped_value

    def email_check(self, email):
        pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.(com|in|net|org|edu)$'
        while True:
            if re.fullmatch(pattern, email):
                return email
            else:
                print("Invalid email!")
                email = input("Enter your email: ")


    def email_exit(self, email):
        ob = Createfile(PathModel.registration_data)
        data = ob.file()
        for i in data:
            if i.get("email") == email:
                print("Email already exists!")
                email = input("\nEnter your email: ")
                email = self.email_check(email)
                return email
        return email

    def address_check(self, address):
        while True:
            if address.isdigit():
                print("Invalid address! Address should not contain only digits.")
                address = input("\nEnter your address: ")
            else:
                return address
    def password_check(self, password):
        while True:
            has_digit = any(ch.isdigit() for ch in password)
            has_alpha = any(ch.isalpha() for ch in password)

            if not (has_digit and has_alpha) or not (8 <= len(password) <= 16):
                print("Invalid password! Password must contain letters, digits and be 8–16 characters long.")
                password = self.enter_password()
            else:
                return password


    def password_exit(self, password):
        ob = Createfile(PathModel.registration_data)
        data = ob.file()
        for i in data:
            if i.get("password") == password:
                print("Password already exists!")
                password = self.enter_password()
                password = self.password_check(password)
                return password
        return password

    def enter_password(self):
        print("Enter your password: ", end="", flush=True)
        password = ""
        while (char := msvcrt.getch()) != b'\r':
            if char == b'\x08' and password:
                password = password[:-1]
                print("\b \b", end="", flush=True)
            elif char != b'\x08':
                password += char.decode()
                print("*", end="", flush=True)
        print()
        return password

    def department_check(self, department):
        while True:
            check = department.replace(" ", "").isalpha()
            if not check:
                print("Invalid department! Department name should contain only characters.")
                department = input("\nEnter your department: ")
            else:
                return department

   
    def past_experience_check(self, pastexperience):
        pattern = r'^([0-9]+)\s*year[s]?$'
        while True:
            pastexperience = pastexperience.strip()
            
            if not pastexperience:
                print("Invalid past experience!")
                pastexperience = input("Enter your past experience (e.g., 2 year): ")
                continue
            
            match = re.fullmatch(pattern, pastexperience, re.IGNORECASE)
            if match:
                number = match.group(1)
                if int(number) > 1:
                    return number + " years"
                else:
                    return number + " year"
            
            if pastexperience.isdigit():
                number = pastexperience
                if int(number) > 1:
                    return number + " years"
                else:
                    return number + " year"
            
            print("Invalid past experience!")
            pastexperience = input("Enter your past experience (e.g., 2 year): ")

    def get_valid_order_id(self,order_id):
        order_id_input = str(order_id).strip()
        while(True):
            if not order_id_input.isdigit() or int(order_id_input) < 101:
                print("invalide id!order id start with 101")
                order_id=input("Enter ID of the order you want to delete: ")
                
            return order_id
            
    def quantity_chcek(self, quantity):
        while True:
            if not quantity.isdigit():
                print("Invalid quantity! quantity should be written in only digit and stock is upto 10 only.")
            elif int(quantity) <= 0:
                print("Invalid quantity! quantity must be greater than 0.")
            elif int(quantity) > 10:
                print("Invalid quantity! quantity should be maximum 10 only.")
            else:
                return quantity

            quantity = input("\nEnter your quantity = ")

    def category_check(self, category):
        allowed = ["Veg", "Non_Veg", "Fast Food", "Drink", "Roti"]

        while True:
            category = category.strip().title()

            if category in allowed:
                return category
            else:
                print("Invalid category!")
                print("Allowed: Veg, Non_Veg, Fast Food, Drink, Roti")
                category = input("enter category of item = ")

        
    def price_check(self, price,prompt):
        while True:
            if price.isdigit() and int(price) > 0:
                return int(price)
            print("Invalid price! Enter a positive number.")
            price = input(prompt)

    def size_check(self, size, item_category):
        while True:
            size_input = size.strip().title()

            if item_category == "roti":
                allowed_sizes = ["Single", "Double"]
                message = "Invalid size! Please enter one of: Single, Double."
                prompt = "Enter size (Single / Double): "
            else:
                allowed_sizes = ["Half", "Full"]
                message = "Invalid size! Please enter one of: Half , Full ."
                prompt = "Enter size (Half  / Full ): "

            if size_input.isnumeric() or size_input not in allowed_sizes:
                print(message)
                size = input(prompt)
            else:
                return size_input

                    
