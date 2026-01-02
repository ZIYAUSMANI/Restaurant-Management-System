import uuid
from ..domain.filehandler import Createfile
from ..validation.checkvalidation import Validationcheck
from ..model.models import UserModel, PathModel , DefaultModel
from ..logs.logger import get_logger

auth_logger = get_logger(PathModel.athu_log, "authentication")

class Signupuser:
    """
    Handles user signup.

    Uses the following classes:
    - Createfile: Handles reading/writing JSON or file data (e.g., user registration).
    - Validetioncheck: Validates all user inputs like name, email, password, address, etc.
    - UserModel: Represents a user with model attributes like id, name, email, password, role, etc.
    - PathModel: Stores file paths for data storage (e.g., registration_data).
    - Default: Access staff model.
    - logger : To handle unexpected error.
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
            
            user.email = validetion_check.email_exit(input("Enter your email: "))
            
            user.password = validetion_check.password_exit(validetion_check.enter_password())
            
            user.address = validetion_check.address_check(input("Enter your address: "))

            user.department = validetion_check.department_check(input("Enter your department: "))

            user.past_experience = Signupuser.collect_experience(validetion_check)

            user.role = DefaultModel.staff
            customer_data = data.file()
            customer_data.append(user.__dict__)
            data.write_in_file(customer_data)
            print("Registered successfully")

        except Exception as e:
            auth_logger.error(
                f"Signup Error | Email: {getattr(user, 'email', 'N/A')} | Error: {e}"
            )
            print("Signup failed")

    
    @staticmethod
    def collect_experience(validetion_check):
        """
        Collects multiple company experience.
        Stores only calculated experience.
        """
        while True:
            has_experience = input("Do you have past experience? (yes/no): ").strip().lower()

            if has_experience == "yes":
                experience_list = []

                while True:
                    company = validetion_check.name_check( input("Enter company name: "), "Enter company name: " )

                    start = validetion_check.date_check(input("Enter start date (YYYY-MM-DD): "))

                    while True:
                        end = validetion_check.date_check(input("Enter end date (YYYY-MM-DD): "))
                        if end < start:
                            print("End date cannot be before start date!")
                            continue
                        break

                    total_months = (end.year - start.year) * 12 + (end.month - start.month)
                    years = total_months // 12
                    months = total_months % 12

                    if months == 0:
                        experience = f"{years} year"
                    else:
                        experience = f"{years} year {months} month"

                    experience_list.append({
                        "company_name": company,
                        "experience": experience
                    })

                    more = input("Do you have more company experience? (yes/no): ").strip().lower()
                    if more != "yes":
                        break

                return experience_list

            elif has_experience == "no":
                return "0 year"

            else:
                print("Invalid input! Please type 'yes' or 'no'.")
