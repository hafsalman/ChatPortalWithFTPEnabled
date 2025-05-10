from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from Authentication.Login import login_user
from Authentication.Register import register_user
from ChatPortal.Server import app as chat_app  # Import full chat system
import os

app = FastAPI()

# Auth Models
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    full_name: str
    username: str
    email: str
    password: str
    phone_number: str = None

# Mount static HTML
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <h1>Welcome to Chat Portal</h1>
    <p>→ <a href='/chat'>Open Web Chat</a></p>
    <p>→ POST to <code>/register</code> or <code>/login</code> with JSON</p>
    """

# Auth Routes
@app.post("/register")
def register_api(request: RegisterRequest):
    return register_user(
        full_name=request.full_name,
        username=request.username,
        email=request.email,
        password=request.password,
        phone_number=request.phone_number
    )

@app.post("/login")
def login_api(request: LoginRequest):
    return login_user(request.username, request.password)

# Include chat routes from Server.py
app.include_router(chat_app.router)

# Run via python Main.py
if __name__ == "_main_":
    import uvicorn
    uvicorn.run("Main:app", host="127.0.0.1", port=8000, reload=True)