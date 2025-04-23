import subprocess
import mysql.connector
import bcrypt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB_Connection.Connection import createConnection

def LoginUser():
    conn = createConnection()

    if conn is None:
        print("Database Connection Failed!")
        return False
    
    cursor = conn.cursor()

    try:
        username = input("Enter Username: ").strip()
        password = input("Enter Password: ").strip()

        cursor.execute("SELECT user_id, username, email, password_hash FROM USERS WHERE username = %s", (username, ))
        user = cursor.fetchone()

        if not user:
            print("Invalid username!")
            return False
        
        user_id, username, email, stored_password = user

        if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            print("Incorrect Password!")
            return False      
        
        print(f"Successful Login! Welcome {username}")
        launch_client(username)

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False
    
    finally:
        cursor.close()
        conn.close()

def launch_client(username):
    try:
        subprocess.run(["python", "ChatPortal\\Client.py", username])
    
    except Exception as e:
        print(f"Failed to launch client chat: {e}")

if __name__ == "__main__":
    if LoginUser():
        print("WHEEEEEEEEEEEEEEEEE")