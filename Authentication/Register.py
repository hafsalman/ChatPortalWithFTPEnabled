import mysql.connector
import bcrypt
import subprocess
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB_Connection.Connection import createConnection

#Change Phone Number and Profile Picture later
# def RegisterUser(full_name, username, email, password, phone_number = None, profile_picture = None):

def RegisterUser():
    conn = createConnection()
    if conn is None:
        print("Database Connection Failed!")
        return False
    
    cursor = conn.cursor()

    try:
        full_name = input("Enter Full Name: ").strip()
        username = input("Enter Username: ").strip()
        email = input("Enter Email: ").strip()
        password = input("Enter Password: ").strip()
        #Change later (Phone Number and Profile Picture)
        phone_number = input("Enter Phone Number (Press Enter to skip): ").strip()
        profile_picture = input("Enter URL for profile picture(Press Enter to skip): ").strip()

        cursor.execute("SELECT * FROM USERS WHERE email = %s", (email, ))
        existingEmail = cursor.fetchone()

        if existingEmail:
            print("Error: This Email already exists!")
            return False
        
        cursor.execute("SELECT * FROM USERS WHERE username = %s", (username, ))
        existingUser = cursor.fetchone()

        if existingUser:
            print("Error: This Username already exists!")
            return False
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        #Inserting User
        cursor.execute("""INSERT INTO USERS (full_name, username, email, password_hash, phone_number, profile_picture) VALUES (%s, %s, %s, %s, %s, %s)""", (full_name, username, email, hashed_password, phone_number, profile_picture))

        conn.commit()

        print("User registered successfully")

        print("Redirecting to the Login page...")

        subprocess.run(["python", os.path.join(os.path.dirname(__file__), "Login.py")])
        return True
    
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False
    
    finally:
        cursor.close()
        conn.close()

#Testing --Change once it works
if __name__ == "__main__":
    RegisterUser()