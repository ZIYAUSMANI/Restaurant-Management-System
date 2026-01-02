from .userlogin import Loginuser
from .usersingup import Signupuser
class UserAuthentication:
    """
    Handles user signup and login.

    Uses the following classes:
    - Loginuser: Access login method.
    - Signupuser Access signup method.
    """

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
                Signupuser.signup()
            elif choice == 2:
                Loginuser.login()
            elif choice == 3:
                print("Thank you!")
                break
            else:
                print("Invalid choice! Please select between 1 to 3.")
