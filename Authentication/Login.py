from DB_Connection.Connection import createConnection
import mysql.connector
import bcrypt
#import threading
#from ChatPortal.Client import StartChat

def login_user(username: str, password: str):
    conn = createConnection()

    if conn is None:
        return {"status": "error", "message": "Database Connection Failed"}
    
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT user_id, username, email, password_hash FROM USERS WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return {"status": "error", "message": "Invalid username"}
        
        user_id, username_db, email, stored_password = user

        if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return {"status": "error", "message": "Incorrect password"}

        #threading.Thread(target=StartChat, args=(username,), daemon=True).start()

        return {"status": "success", "message": f"Welcome {username_db}"}
    
    except mysql.connector.Error as err:
        return {"status": "error", "message": f"Database error: {err}"}
    
    finally:
        cursor.close()
        conn.close()