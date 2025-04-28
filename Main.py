import os
import subprocess
import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from DB_Connection.Connection import createConnection
from Authentication.Login import login_user
from Authentication.Register import RegisterUser

app = FastAPI()

current_dir = os.path.dirname(__file__)
register_script = os.path.join(current_dir, "Authentication", "Register.py")
login_script = os.path.join(current_dir, "Authentication", "Login.py")

@app.get("/")
def welcome():
    return {
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
        RegisterUser()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/login")
def login():
    try:
        login_user()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run("Main:app", host="127.0.0.1", port=8000, reload=True)