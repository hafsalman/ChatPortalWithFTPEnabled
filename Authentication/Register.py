import mysql.connector
import bcrypt
from DB_Connection.Connection import createConnection

def register_user(full_name: str, username: str, email: str, password: str, phone_number: str = None, profile_picture: str = None):
    conn = createConnection()
    if conn is None:
        return {"status": "error", "message": "Database Connection Failed"}

    cursor = conn.cursor()

    try:
        # Check for existing email
        cursor.execute("SELECT * FROM USERS WHERE email = %s", (email,))
        existing_email = cursor.fetchone()
        if existing_email:
            return {"status": "error", "message": "Email already exists"}

        # Check for existing username
        cursor.execute("SELECT * FROM USERS WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            return {"status": "error", "message": "Username already exists"}

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Insert new user
        cursor.execute("""
            INSERT INTO USERS (full_name, username, email, password_hash, phone_number, profile_picture) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (full_name, username, email, hashed_password, phone_number, profile_picture))

        conn.commit()

        return {"status": "success", "message": "User registered successfully"}

    except mysql.connector.Error as err:
        return {"status": "error", "message": f"Database error: {err}"}

    finally:
        cursor.close()
        conn.close()