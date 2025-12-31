import re
import msvcrt
from ..domain.filehandler import Createfile
from ..model.models import PathModel

class Validationcheck:
    def name_check(self, name):
        while True:
            stripped_name = name.strip()

            if not (3 <= len(stripped_name) <= 20):
                print("Invalid name! Length must be between 3 and 20 characters.")
                name = input("Enter your name: ")
                continue

            if stripped_name.count(" ") > 2:
                print("Invalid name! Only up to 2 spaces are allowed.")
                name = input("Enter your name: ")
                continue

            if not stripped_name.replace(" ", "").isalpha():
                print("Invalid name! Name should contain only letters.")
                name = input("Enter your name: ")
                continue

            letters_only = stripped_name.replace(" ", "").lower()
            if len(set(letters_only)) == 1:
                print("Invalid name! Name cannot contain the same letter repeatedly.")
                name = input("Enter your name: ")
                continue

            return stripped_name

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

    def id_chcek(self,id):
        food=Createfile(PathModel.food_data)
        food_menu=food.file()
        last_id=int(food_menu["DINNER"][-1]["id"])
        while True:
            id_chcek=id.isdigit() 
            if id_chcek==False or int(id)>last_id or int(id)<=0:
                print(f"Invalid id! id should have only digit and there are only {last_id} items.")
                id=input("\nenter the id of item =")
            else:
                return id
    def quantity_chcek(self,quantity):
        while True:
            quantity_chcek=quantity.isdigit() 
            if quantity_chcek==False or int(quantity)>=11:
                print("Invalid quantity! quantity should be written in only digit and stock is upto 10 only.")
                quantity=input("\nEnter your quantity =")
            else:
                return quantity
            
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

        
    def price_check(self, price):
        while True:
            if price.isdigit() and int(price) > 0:
                return int(price)
            print("Invalid price! Enter a positive number.")
            price = input("enter the price of item = ")
