import mysql.connector

def createConnection():
    try: 
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="abc123",
            database="CN_PROJECT"
        )

        if conn.is_connected(): 
            print("Database is connected successfully!")
            return conn

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None