import re
import msvcrt
from ..domain.filehandler import Createfile
from ..model.models import PathModel
from datetime import datetime

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


    def email_exit(self,email):
        ob = Createfile(PathModel.registration_data)
        data = ob.file()
        email = self.email_check(email)
        while True:
            email_found = False
            for i in data:
                if i.get("email") == email:
                    print("Email already exists!")
                    email = input("\nEnter your email: ")
                    email = self.email_check(email)
                    email_found = True
                    break
                    
            if not email_found:
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


    def password_exit(self,password):
        password = self.password_check(password)
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

    def date_check(self,date_value):
        """
        Validates date input in YYYY-MM-DD format.
        Accepts only years between 2000 and current year.
        """
        min_year = 2000
        max_year = datetime.now().year

        while True:
            try:
                date_obj = datetime.strptime(date_value, "%Y-%m-%d")

                if date_obj.year < min_year or date_obj.year > max_year:
                    print(f"Year must be between {min_year} and {max_year}")
                    date_value = input()
                    continue

                return date_obj

            except ValueError:
                print("Invalid date format! Use YYYY-MM-DD")
                date_value = input()


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

    def size_check(self,size_input, allowed_sizes):
        
        while True:
            if size_input.lower() in allowed_sizes:
                return size_input.title()
            else:
                print("Invalid size! Choose only from:")
                for size in allowed_sizes:
                    print(f"- {size.title()}")
                size_input = input("Enter size again: ").strip()


    def validate_card_number(self,card_number):
        while True:
            
            if card_number.isdigit() and 13 <= len(card_number) <= 19:
                return card_number
            print("Invalid Card Number! It should be 13-19 digits.")
            card_number = input("Enter Card Number:").strip()

    def validate_expiry_date(self,expiry_date):
        while True:
            try:
                exp_month, exp_year = expiry_date.split("/")
                if not (exp_month.isdigit() and exp_year.isdigit()):
                    raise ValueError
                exp_month = int(exp_month)
                exp_year = int("20" + exp_year)
                now = datetime.now()
                if 1 <= exp_month <= 12 and ((exp_year > now.year) or (exp_year == now.year and exp_month >= now.month)):
                    return expiry_date
                else:
                    raise ValueError
            except ValueError:
                expiry_date = input("Enter Expiry Date (MM/YY):").strip()
                print("Invalid Expiry Date! Ensure MM/YY format and not expired.")

    def validate_cvv(self, cvv):
        while True:
            if cvv.isdigit() and len(cvv) in (3, 4):
                if int(cvv) != 0:
                    return cvv

            print("Invalid CVV! It should be 3 or 4 digits and cannot be all zeros.")
            cvv = input("Enter CVV: ").strip()

    def validate_upi(self,upi_id):
        allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_@")
        while True:
            if upi_id and "@" in upi_id and all(char in allowed_chars for char in upi_id):
                return upi_id
            print("Invalid UPI ID! Must contain '@' and valid characters.")
            upi_id = input("Enter UPI ID:").strip()

