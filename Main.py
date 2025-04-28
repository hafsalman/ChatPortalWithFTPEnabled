from fastapi import FastAPI
from pydantic import BaseModel
from Authentication.Login import login_user
from Authentication.Register import RegisterUser  # assuming you have similar register function

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

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
def login_api(request: LoginRequest):
    result = login_user(request.username, request.password)
    return result