# import os
# import subprocess
# from DB_Connection.Connection import createConnection

# def main():
#     while True:
#         print("Welcome to Chat Portal")
#         print("1. Register")
#         print("2. Login")
        
#         choice = input("Choice: ").strip()

#         if choice == "1":
#             print("Registration Page!")
#             subprocess.run(["python", os.path.join(os.path.dirname(__file__), "Authentication", "Register.py")])

#         elif choice == "2":
#             print("Login Page!")
#             subprocess.run(["python", os.path.join(os.path.dirname(__file__), "Authentication", "Login.py")])

#         else:
#             print("Invalid choice!")

# if __name__ == "__main__":
#     main()

from fastapi import FastAPI
from Authentication.Register import RegisterUser
from Authentication.Login import login_user

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Chat Portal. Visit /register or /login"}

@app.post("/register")
def register_user():
    try:
        RegisterUser()
        return {"status": "success", "message": "Registration completed"}
    except Exception as e:
        return {"status": "error", "message": f"Registration failed: {str(e)}"}

@app.post("/login")
def LoginUser():
    try:
        login_user()
        return {"status": "success", "message": "Login completed"}
    except Exception as e:
        return {"status": "error", "message": f"Login failed: {str(e)}"}