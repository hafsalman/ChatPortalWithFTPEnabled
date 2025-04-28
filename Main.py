import os
import subprocess
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <html>
        <head>
            <title>Chat Portal</title>
        </head>
        <body style="font-family: Arial, sans-serif;">
            <h2>Welcome to Chat Portal</h2>
            <form action="/register" method="post">
                <input type="submit" value="Register" style="padding:10px; margin:5px;">
            </form>
            <form action="/login" method="post">
                <input type="submit" value="Login" style="padding:10px; margin:5px;">
            </form>
        </body>
    </html>
    """

@app.post("/register", response_class=HTMLResponse)
async def register():
    subprocess.run(["python", os.path.join(os.path.dirname(__file__), "Authentication", "Register.py")])
    return """
    <html>
        <body>
            <h3>✅ Registration Completed Successfully!</h3>
            <a href="/">Go Back</a>
        </body>
    </html>
    """

@app.post("/login", response_class=HTMLResponse)
async def login():
    subprocess.run(["python", os.path.join(os.path.dirname(__file__), "Authentication", "Login.py")])
    return """
    <html>
        <body>
            <h3>✅ Login Attempted. Please Check Console.</h3>
            <a href="/">Go Back</a>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run("Main:app", host="127.0.0.1", port=8000, reload=True)