import os
import subprocess
from DB_Connection.Connection import createConnection

def main():
    while True:
        print("Welcome to Chat Portal")
        print("1. Register")
        print("2. Login")
        
        choice = input("Choice: ").strip()

        if choice == "1":
            print("Registration Page!")
            subprocess.run(["python", os.path.join(os.path.dirname(__file__), "Authentication", "Register.py")])

        elif choice == "2":
            print("Login Page!")
            subprocess.run(["python", os.path.join(os.path.dirname(__file__), "Authentication", "Login.py")])

        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()