import uuid
from ..domain.filehandler import Createfile
from ..validation.checkvalidation import Validationcheck
from ..model.models import UserModel, PathModel
from ..domain.adminmenu import Menuadmin
from ..domain.staffmenu import Menustaff
from ..logs.logger import logger


class UserAuthentication:
    """
    Handles user signup and login.

    Uses the following classes:
    - Createfile: Handles reading/writing JSON or file data (e.g., user registration).
    - Validetioncheck: Validates all user inputs like name, email, password, address, etc.
    - UserModel: Represents a user with model attributes like id, name, email, password, role, etc.
    - PathModel: Stores file paths for data storage (e.g., registration_data).
    - Menuadmin: Access admin dashboard.
    - Menustaff: Access staff dashboard.
    """

    @staticmethod
    def signup():
        """Register a new user."""
        validetion_check = Validationcheck()
        user = UserModel()
        data = Createfile(PathModel.registration_data)

        try:
            user.id = uuid.uuid4().hex[:8]
            user.name = validetion_check.name_check(input("Enter your user name: "),"Enter your user name: ")
            user.email = validetion_check.email_exit(
                validetion_check.email_check(input("Enter your email: "))
            )
            user.password = validetion_check.password_exit(
                validetion_check.password_check(validetion_check.enter_password())
            )
            user.address = validetion_check.address_check(input("Enter your address: "))
            user.department = validetion_check.department_check(input("Enter your department: "))

            while True:
                has_experience = input("Do you have past experience? (yes/no): ").strip().lower()
                if has_experience == "yes":
                    user.past_experience = validetion_check.past_experience_check(
                        input("Enter your past experience (e.g., 2 year): ")
                    )
                    break
                elif has_experience == "no":
                    user.past_experience = "0 year"
                    break
                else:
                    print("Invalid input! Please type 'yes' or 'no'.")

            user.role = "staff"
            customer_data = data.file()
            customer_data.append(user.__dict__)
            data.write_in_file(customer_data)
            print("Registered successfully")

        except Exception as e:
            logger.error(
                f"Signup Error | Email: {getattr(user, 'email', 'N/A')} | Error: {e}"
            )
            print("Signup failed")
            
    @staticmethod
    def login():
        """Login a user"""
        validetion_check = Validationcheck()
        data = Createfile(PathModel.registration_data)
        customer_data = data.file()

        try:
            user_email = validetion_check.email_check(input("Enter your email: "))
            user_password = validetion_check.password_check(
                validetion_check.enter_password()
            )

            email_valid = False
            password_valid = False
            user_role = None

            for user_record in customer_data:
                if user_record["email"] == user_email:
                    email_valid = True
                    if user_record["password"] == user_password:
                        password_valid = True
                        user_role = user_record["role"]
                    break

            if not email_valid:
                print("Invalid email!")
                return

            if not password_valid:
                print("Invalid password!")
                return

            print("Login successfully!")
            if user_role == "admin":
                Menuadmin.admindasbord()
            else:
                Menustaff.staffdasbord()

        except Exception as e:
            logger.error(
                f"LOGIN FAILED AFTER VALID INPUT | Email: {user_email} | Error: {e}"
            )
            print("Login failed due to system error")


    @staticmethod
    def authentication_menu():
        """Display signup/login/exit menu for user."""
        while True:
            print("""\n|================================================|
|               REGISTRATION MENU                |
|================================================|
|   1. SIGNUP                                    |
|   2. LOGIN                                     |
|   3. EXIT                                      |
|================================================|""")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input! Only numbers are allowed.")
                continue

            if choice == 1:
                UserAuthentication.signup()
            elif choice == 2:
                UserAuthentication.login()
            elif choice == 3:
                print("Thank you!")
                break
            else:
                print("Invalid choice! Please select between 1 to 3.")
