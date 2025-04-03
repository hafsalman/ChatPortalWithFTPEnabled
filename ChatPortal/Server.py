import asyncio
import websocket
import mysql.connector
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB_Connection.Connection import createConnection

session = {}

def MessageHistory():
    conn = createConnection()

    if conn is None:
        return[]
    
    cursor = conn.cursor(dictionary = True)
    
    try:
        cursor.execute("""SELECT sender, reciever, message, m_time FROM MESSAGES WHERE (sender = %s AND receiver = %s) OR (receiver = %s AND sender = %s) ORDER BY m_time ASC""", (user1, user2, user2, user1))

        messages = cursor.fetchall()

        return messages
    
    except Exception as err:
        print(f"Database Error: {err}")

        return[]
    
    finally:
        cursor.close()
        conn.close()

async def HandleClient(websocket, path):
    login_data = websocket.recv()
    user_info = json.loads(login_data)
    username = user_info["username"]

    session[username] = websocket
    print(f"{username} MEOWED")

    conn = createConnection()

    if conn:
        cursor = conn.cursor()

        cursor.execute("SELECT DISTINCT sender, receiver WHERE sender = %s OR receiver = %s", (username, username))

        contacts = cursor.fetchall()

        cursor.close()
        conn.close()

        for contact in contacts:
            chatPartner = contact[0] if contact[0] != username else contact[1]