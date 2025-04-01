import mysql.connector
from DB_Connection.Connection import createConnection
import bcrypt

#Change Phone Number and Profile Picture later
def RegisterUser(full_name, username, email, password, phone_number = None, profile_picture = None):
    conn = createConnection()
    if conn is None:
        print("Database Connection Failed!")
        return False
    
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM USERS WHERE email = %s", email)
        existingEmail = cursor.fetchone()

        if existingEmail:
            print("Error: This Email already exists!")
            return False
        
        cursor.execute("SELECT * FROM USERS WHERE username = %s", username)
        existingUser = cursor.fetchone()

        if existingUser:
            print("Error: This Username already exists!")
            return False
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        