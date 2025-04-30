from fastapi import FastAPI
from pydantic import BaseModel
from Authentication.Login import login_user
from Authentication.Register import register_user

app = FastAPI()

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    full_name: str
    username: str
    email: str
    password: str
    phone_number: str = None
    #profile_picture: str = None

@app.get("/")
def home():
    return {"message": "Welcome to Chat Portal. Visit /register or /login"}

@app.post("/register")
def register_api(request: RegisterRequest):
    result = register_user(
        full_name=request.full_name,
        username=request.username,
        email=request.email,
        password=request.password,
        phone_number=request.phone_number,
        #profile_picture=request.profile_picture
    )
    return result

@app.post("/login")
def login_api(request: LoginRequest):
    result = login_user(request.username, request.password)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Main:app", host="127.0.0.1", port=8001, reload=True)