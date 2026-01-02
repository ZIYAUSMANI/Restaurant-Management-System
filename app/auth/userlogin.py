from ..domain.filehandler import Createfile
from ..validation.checkvalidation import Validationcheck
from ..model.models import PathModel , DefaultModel
from ..domain.adminmenu import Menuadmin
from ..domain.staffmenu import Menustaff
from ..logs.logger import get_logger

auth_logger = get_logger(PathModel.athu_log, "authentication")

class Loginuser:
    """
    Handles user login.

    Uses the following classes:
    - Createfile: Handles reading/writing JSON or file data (e.g., user registration).
    - Validetioncheck: Validates all user inputs like name, email, password, address, etc.
    - PathModel: Stores file paths for data storage (e.g., registration_data).
    - Default: Access admin model.
    - Menuadmin: Access admin dashboard.
    - Menustaff: Access staff dashboard.
    - logger: To handle anexpected errorr. 
    """
    @staticmethod
    def login():
        """Login a user"""
        validetion_check = Validationcheck()
        data = Createfile(PathModel.registration_data)
        customer_data = data.file()

        try:
            user_email = validetion_check.email_check(input("Enter your email: "))
            
            user_password = validetion_check.password_check(validetion_check.enter_password())

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
            if user_role == DefaultModel.admin:
                Menuadmin.admindasbord()
            else:
                Menustaff.staffdasbord()

        except Exception as e:
            auth_logger.error(
                f"LOGIN FAILED AFTER VALID INPUT | Email: {user_email} | Error: {e}"
            )
            print("Login failed")


    