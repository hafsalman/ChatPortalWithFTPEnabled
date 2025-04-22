# import asyncio
# import websocket
# import mysql.connector
# import json
# import sys
# import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from DB_Connection.Connection import createConnection

# session = {}

# def MessageHistory():
#     conn = createConnection()

#     if conn is None:
#         return[]
    
#     cursor = conn.cursor(dictionary = True)
    
#     try:
#         #cursor.execute("""SELECT sender, reciever, message, m_time FROM MESSAGES WHERE (sender = %s AND receiver = %s) OR (receiver = %s AND sender = %s) ORDER BY m_time ASC""", (user1, user2, user2, user1))

#         messages = cursor.fetchall()

#         return messages
    
#     except Exception as err:
#         print(f"Database Error: {err}")

#         return[]
    
#     finally:
#         cursor.close()
#         conn.close()

# async def HandleClient(websocket, path):
#     login_data = websocket.recv()
#     user_info = json.loads(login_data)
#     username = user_info["username"]

#     session[username] = websocket
#     print(f"{username} MEOWED")

#     conn = createConnection()

#     if conn:
#         cursor = conn.cursor()

#         cursor.execute("SELECT DISTINCT sender, receiver WHERE sender = %s OR receiver = %s", (username, username))

#         contacts = cursor.fetchall()

#         cursor.close()
#         conn.close()

#         for contact in contacts:
#             chatPartner = contact[0] if contact[0] != username else contact[1]

import socket
import threading
import mysql.connector
from DB_Connection.Connection import createConnection

clients = {}

def handle_client(conn, addr):
    conn.send("Username: ".encode())
    username = conn.recv(1024).decode()
    clients[username] = conn

    print(f"[{username}] connected from {addr}")

    try:
        while True:
            msg = conn.recv(1024).decode()
            if msg.lower() == "exit":
                break

            if ":" in msg:
                receiver, message = msg.split(":", 1)
                receiver = receiver.strip()
                message = message.strip()

                save_message(username, receiver, message)

                if receiver in clients:
                    clients[receiver].send(f"[{username}] {message}".encode())
                else:
                    conn.send(f"{receiver} is not online.".encode())
            else:
                conn.send("Invalid format. Use: receiver: message".encode())
    except:
        pass
    finally:
        print(f"[{username}] disconnected.")
        conn.close()
        clients.pop(username, None)

def save_message(sender, receiver, message):
    conn = createConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO MESSAGES (sender, receiver, message)
            VALUES (%s, %s, %s)
        """, (sender, receiver, message))
        conn.commit()
        cursor.close()
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("localhost", 12345))
    server.listen()
    print("[Server] Listening on port 12345...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()