import mysql.connector
import bcrypt
import sys
import os
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

        cursor.execute("SELECT user_id, username, password_hash FROM USERS WHERE username = %s", (username, ))
        user = cursor.fetchone()

        if not user:
            print("Invalid username!")
            return False
        
        username, password = user

        if not 