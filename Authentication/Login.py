# import subprocess
# import mysql.connector
# import bcrypt
# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from DB_Connection.Connection import createConnection

# def LoginUser():
#     conn = createConnection()

#     if conn is None:
#         print("Database Connection Failed!")
#         return False
    
#     cursor = conn.cursor()

#     try:
#         username = input("Enter Username: ").strip()
#         password = input("Enter Password: ").strip()

#         cursor.execute("SELECT user_id, username, email, password_hash FROM USERS WHERE username = %s", (username, ))
#         user = cursor.fetchone()

#         if not user:
#             print("Invalid username!")
#             return False
        
#         user_id, username, email, stored_password = user

#         if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
#             print("Incorrect Password!")
#             return False      
        
#         print(f"Successful Login! Welcome {username}")
#         launch_client(username)

#     except mysql.connector.Error as err:
#         print(f"Database error: {err}")
#         return False
    
#     finally:
#         cursor.close()
#         conn.close()

# def launch_client(username):
#     try:
#         subprocess.run(["python", "ChatPortal\\Client.py", username])
    
#     except Exception as e:
#         print(f"Failed to launch client chat: {e}")

# if __name__ == "__main__":
#     if LoginUser():
#         print("WHEEEEEEEEEEEEEEEEE")

import subprocess
import mysql.connector
import bcrypt
import sys
import os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import uvicorn

# Set path for DB connection
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB_Connection.Connection import createConnection

app = FastAPI()

def login_user(username: str, password: str):
    conn = createConnection()

    if conn is None:
        return "❌ Database Connection Failed!"
    
    cursor = conn.cursor()

    try:
        # Fetch user data
        cursor.execute("SELECT user_id, username, email, password_hash FROM USERS WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return "❌ Invalid username!"
        
        user_id, db_username, email, stored_password = user

        if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return "❌ Incorrect password!"
        
        # Successful login
        launch_client(db_username)
        return f"✅ Successful Login! Welcome {db_username}"

    except mysql.connector.Error as err:
        return f"❌ Database error: {err}"
    
    finally:
        cursor.close()
        conn.close()

def launch_client(username):
    try:
        subprocess.Popen(["python", os.path.join(os.path.dirname(__file__), '..', "ChatPortal", "Client.py"), username])
    except Exception as e:
        print(f"❌ Failed to launch chat client: {e}")

@app.get("/", response_class=HTMLResponse)
async def login_page():
    return """
    <h2>Login to Chat Portal</h2>
    <form action="/login" method="post">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <input type="submit" value="Login">
    </form>
    """

@app.post("/login", response_class=HTMLResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    result = login_user(username, password)
    return f"<h3>{result}</h3><br><a href='/'>Go back</a>"

if __name__ == "__main__":
    uvicorn.run("Authentication.Login:app", host="127.0.0.1", port=8001, reload=True)