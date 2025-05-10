from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from Authentication.Login import login_user
from Authentication.Register import register_user
from ChatPortal.Server import app as chat_app
from fastapi import Form
import uvicorn
    
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

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chat Portal</title>
        <style>
            :root {
                --bg-primary: #1a1a1a;
                --bg-secondary: #252525;
                --text-primary: #e0e0e0;
                --text-secondary: #a0a0a0;
                --accent: #7289da;
                --accent-hover: #5f73bc;
                --border: #3a3a3a;
            }
            
            body {
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: var(--bg-primary);
                color: var(--text-primary);
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                text-align: center;
            }
            
            .container {
                background: var(--bg-secondary);
                border-radius: 12px;
                padding: 40px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.2);
                border: 1px solid var(--border);
                max-width: 500px;
                width: 90%;
            }
            
            h1 {
                margin-top: 0;
                color: var(--text-primary);
                font-weight: 600;
                margin-bottom: 24px;
            }
            
            p {
                margin: 16px 0;
                font-size: 16px;
            }
            
            .btn {
                color: var(--text-primary);
                text-decoration: none;
                padding: 12px 24px;
                background: var(--accent);
                border-radius: 8px;
                transition: all 0.2s ease;
                display: inline-block;
                margin: 10px;
                font-weight: 500;
                border: none;
                cursor: pointer;
            }
            
            .btn:hover {
                background: var(--accent-hover);
                transform: translateY(-2px);
            }
            
            .btn-secondary {
                background: rgba(114, 137, 218, 0.2);
            }
            
            .btn-secondary:hover {
                background: rgba(114, 137, 218, 0.3);
            }
            
            .logo {
                font-size: 36px;
                margin-bottom: 20px;
            }
            
            .buttons {
                margin-top: 20px;
            }
            
            .api-info {
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid var(--border);
                font-size: 14px;
                color: var(--text-secondary);
            }
            
            code {
                background: var(--bg-primary);
                padding: 4px 8px;
                border-radius: 4px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🌌</div>
            <h1>Welcome to Chat Portal</h1>
            <p>Connect with others in real-time through our secure chat platform</p>
            
            <div class="buttons">
                <a href="/login" class="btn">Login</a>
                <a href="/register" class="btn btn-secondary">Register</a>
            </div>
            
            <div class="api-info">
                <p>API: POST to <code>/register</code> or <code>/login</code> with JSON</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.get("/register", response_class=HTMLResponse)
def register_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Register - Chat Portal</title>
        <style>
            :root {
                --bg-primary: #1a1a1a;
                --bg-secondary: #252525;
                --text-primary: #e0e0e0;
                --text-secondary: #a0a0a0;
                --accent: #7289da;
                --accent-hover: #5f73bc;
                --border: #3a3a3a;
                --error: #f04747;
                --success: #43b581;
            }
            
            body {
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: var(--bg-primary);
                color: var(--text-primary);
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }
            
            .container {
                background: var(--bg-secondary);
                border-radius: 12px;
                padding: 40px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.2);
                border: 1px solid var(--border);
                max-width: 500px;
                width: 90%;
            }
            
            h1 {
                margin-top: 0;
                color: var(--text-primary);
                font-weight: 600;
                margin-bottom: 24px;
                text-align: center;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
            }
            
            input {
                width: 100%;
                padding: 12px;
                background: var(--bg-primary);
                border: 1px solid var(--border);
                border-radius: 6px;
                color: var(--text-primary);
                font-size: 16px;
                transition: all 0.2s ease;
                box-sizing: border-box;
            }
            
            input:focus {
                border-color: var(--accent);
                outline: none;
                box-shadow: 0 0 0 2px rgba(114, 137, 218, 0.3);
            }
            
            .btn {
                width: 100%;
                padding: 14px;
                background: var(--accent);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                margin-top: 10px;
            }
            
            .btn:hover {
                background: var(--accent-hover);
                transform: translateY(-2px);
            }
            
            .btn:active {
                transform: translateY(0);
            }
            
            .logo {
                font-size: 36px;
                margin-bottom: 20px;
                text-align: center;
            }
            
            .message {
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 20px;
                display: none;
            }
            
            .error {
                background: rgba(240, 71, 71, 0.1);
                color: var(--error);
                border: 1px solid rgba(240, 71, 71, 0.3);
            }
            
            .success {
                background: rgba(67, 181, 129, 0.1);
                color: var(--success);
                border: 1px solid rgba(67, 181, 129, 0.3);
            }
            
            .login-link {
                text-align: center;
                margin-top: 20px;
            }
            
            .login-link a {
                color: var(--accent);
                text-decoration: none;
            }
            
            .login-link a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🌌</div>
            <h1>Create an Account</h1>
            
            <div id="message" class="message"></div>
            
            <form id="register-form">
                <div class="form-group">
                    <label for="full_name">Full Name</label>
                    <input type="text" id="full_name" name="full_name" required>
                </div>
                
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <div class="form-group">
                    <label for="phone_number">Phone Number (Optional)</label>
                    <input type="tel" id="phone_number" name="phone_number">
                </div>
                
                <button type="submit" class="btn">Register</button>
            </form>
            
            <div class="login-link">
                Already have an account? <a href="/login">Login</a>
            </div>
        </div>
        
        <script>
            document.getElementById('register-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const messageEl = document.getElementById('message');
                messageEl.style.display = 'none';
                messageEl.className = 'message';
                
                const formData = {
                    full_name: document.getElementById('full_name').value,
                    username: document.getElementById('username').value,
                    email: document.getElementById('email').value,
                    password: document.getElementById('password').value,
                    phone_number: document.getElementById('phone_number').value || null
                };
                
                try {
                    const response = await fetch('/register', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(formData)
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        messageEl.textContent = 'Registration successful! Redirecting to login...';
                        messageEl.classList.add('success');
                        messageEl.style.display = 'block';
                        
                        // Redirect to login page after 2 seconds
                        setTimeout(() => {
                            window.location.href = '/login';
                        }, 2000);
                    } else {
                        messageEl.textContent = data.detail || 'Registration failed. Please try again.';
                        messageEl.classList.add('error');
                        messageEl.style.display = 'block';
                    }
                } catch (error) {
                    messageEl.textContent = 'An error occurred. Please try again.';
                    messageEl.classList.add('error');
                    messageEl.style.display = 'block';
                }
            });
        </script>
    </body>
    </html>
    """

@app.get("/login", response_class=HTMLResponse)
def login_page():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login - Chat Portal</title>
        <style>
            :root {
                --bg-primary: #1a1a1a;
                --bg-secondary: #252525;
                --text-primary: #e0e0e0;
                --text-secondary: #a0a0a0;
                --accent: #7289da;
                --accent-hover: #5f73bc;
                --border: #3a3a3a;
                --error: #f04747;
                --success: #43b581;
            }
            
            body {
                font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: var(--bg-primary);
                color: var(--text-primary);
                margin: 0;
                padding: 0;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
            }
            
            .container {
                background: var(--bg-secondary);
                border-radius: 12px;
                padding: 40px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.2);
                border: 1px solid var(--border);
                max-width: 500px;
                width: 90%;
            }
            
            h1 {
                margin-top: 0;
                color: var(--text-primary);
                font-weight: 600;
                margin-bottom: 24px;
                text-align: center;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 500;
            }
            
            input {
                width: 100%;
                padding: 12px;
                background: var(--bg-primary);
                border: 1px solid var(--border);
                border-radius: 6px;
                color: var(--text-primary);
                font-size: 16px;
                transition: all 0.2s ease;
                box-sizing: border-box;
            }
            
            input:focus {
                border-color: var(--accent);
                outline: none;
                box-shadow: 0 0 0 2px rgba(114, 137, 218, 0.3);
            }
            
            .btn {
                width: 100%;
                padding: 14px;
                background: var(--accent);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                margin-top: 10px;
            }
            
            .btn:hover {
                background: var(--accent-hover);
                transform: translateY(-2px);
            }
            
            .btn:active {
                transform: translateY(0);
            }
            
            .logo {
                font-size: 36px;
                margin-bottom: 20px;
                text-align: center;
            }
            
            .message {
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 20px;
                display: none;
            }
            
            .error {
                background: rgba(240, 71, 71, 0.1);
                color: var(--error);
                border: 1px solid rgba(240, 71, 71, 0.3);
            }
            
            .success {
                background: rgba(67, 181, 129, 0.1);
                color: var(--success);
                border: 1px solid rgba(67, 181, 129, 0.3);
            }
            
            .register-link {
                text-align: center;
                margin-top: 20px;
            }
            
            .register-link a {
                color: var(--accent);
                text-decoration: none;
            }
            
            .register-link a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="logo">🌌</div>
            <h1>Login to Chat Portal</h1>
            
            <div id="message" class="message"></div>
            
            <form id="login-form">
                <div class="form-group">
                    <label for="username">Username</label>
                    <input type="text" id="username" name="username" required>
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required>
                </div>
                
                <button type="submit" class="btn">Login</button>
            </form>
            
            <div class="register-link">
                Don't have an account? <a href="/register">Register</a>
            </div>
        </div>
        
        <script>
            document.getElementById('login-form').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const messageEl = document.getElementById('message');
                messageEl.style.display = 'none';
                messageEl.className = 'message';
                
                const formData = {
                    username: document.getElementById('username').value,
                    password: document.getElementById('password').value
                };
                
                try {
                    const response = await fetch('/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(formData)
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        messageEl.textContent = 'Login successful! Redirecting to chat...';
                        messageEl.classList.add('success');
                        messageEl.style.display = 'block';
                        
                        // Store the username for the chat
                        localStorage.setItem('username', formData.username);
                        
                        // Redirect to chat page after 1 second
                        setTimeout(() => {
                            window.location.href = '/chat?username=' + encodeURIComponent(formData.username);
                        }, 1000);
                    } else {
                        messageEl.textContent = data.detail || 'Login failed. Please check your credentials.';
                        messageEl.classList.add('error');
                        messageEl.style.display = 'block';
                    }
                } catch (error) {
                    messageEl.textContent = 'An error occurred. Please try again.';
                    messageEl.classList.add('error');
                    messageEl.style.display = 'block';
                }
            });
        </script>
    </body>
    </html>
    """

@app.post("/register")
def register_api(request: RegisterRequest):
    return register_user(
        username=request.username,
        full_name=request.full_name,
        email=request.email,
        password=request.password
    )
@app.post("/login")
def login_api(request: LoginRequest):
    return login_user(request.username, request.password)

app.include_router(chat_app.router)

if __name__ == "__main__":
    uvicorn.run("Main:app", host="127.0.0.1", port=8000, reload=True)