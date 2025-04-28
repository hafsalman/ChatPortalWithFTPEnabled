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
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

# Allow imports from parent directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB_Connection.Connection import createConnection

app = FastAPI()

# Pydantic model for input validation
class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login_user(request: LoginRequest):
    conn = createConnection()

    if conn is None:
        raise HTTPException(status_code=500, detail="Database Connection Failed!")

    cursor = conn.cursor()

    try:
        username = request.username.strip()
        password = request.password.strip()

        cursor.execute("SELECT user_id, username, email, password_hash FROM USERS WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid username!")

        user_id, db_username, email, stored_password = user

        if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            raise HTTPException(status_code=401, detail="Incorrect password!")

        # Successful login
        # Launch client in a subprocess (optional - usually not triggered from API servers, but okay for your case)
        try:
            launch_client(username)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to launch chat client: {e}")

        return JSONResponse(content={"message": f"Successful Login! Welcome {username}"}, status_code=200)

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database error: {err}")

    finally:
        cursor.close()
        conn.close()

def launch_client(username):
    try:
        subprocess.run(["python", "ChatPortal/Client.py", username])
    except Exception as e:
        raise Exception(f"Failed to launch client: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("Authentication.Login:app", host="127.0.0.1", port=8001, reload=True)