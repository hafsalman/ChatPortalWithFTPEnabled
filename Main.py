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

import os
import subprocess
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from DB_Connection.Connection import createConnection

app = FastAPI()

# Paths
current_dir = os.path.dirname(__file__)
register_script = os.path.join(current_dir, "Authentication", "Register.py")
login_script = os.path.join(current_dir, "Authentication", "Login.py")

@app.get("/")
def welcome():
    return 
    {
        "message": "Welcome to Chat Portal!",
        "options": 
        {
            "1": "Register - visit /register",
            "2": "Login - visit /login"
        }
    }

@app.post("/register")
def register():
    try:
        result = subprocess.run(["python", register_script], capture_output=True, text=True)
        return JSONResponse(content={"output": result.stdout}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/login")
def login():
    try:
        result = subprocess.run(["python", login_script], capture_output=True, text=True)
        return JSONResponse(content={"output": result.stdout}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("Main:app", host="127.0.0.1", port=8000, reload=True)