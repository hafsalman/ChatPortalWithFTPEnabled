# import socket
# import threading 
# import sys
# import os
# import mysql.connector
# from datetime import datetime

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from DB_Connection.Connection import createConnection

# HOST = '127.0.0.1'
# PORT = 5555

# def ShowHistory(username):
#     conn = createConnection()

#     if conn is None:
#         print("Couldn't connect to the Database!")
#         return
    
#     try:
#         cursor = conn.cursor()

#         cursor.execute("""SELECT sender, reciever, messafe, m_time FROM MESSAGES WHERE (sender = %s AND receiver = 'server') OR (sender = 'server' AND receiver = %s) ORDER BY  m_time ASC""", (username, username))
#         for row in cursor.fetchall():
#             sender, receiver, message, timestamp = row
#             print(f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {sender}: {message}")

#     except Exception as e:
#         print("History couldn't be loaded!")

#     finally:
#         cursor.close()
#         conn.close()

# def ReceiveMessage(sock):
#     while True:
#         try:
#             message = sock.recv(1024).decode('utf-8')

#             if message:
#                 print(f"\n{message} \nClient: ", end="", flush=True)

#             else:
#                 break

#         except:
#             print("Connection Lost!")
#             break

# def StartChat(username):
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     try:
#         client.connect((HOST, PORT))

#     except Exception as e:
#         print(f"Connection failed: {e}")
#         return
    
#     client.send(username.encode('utf-8'))

#     ShowHistory(username)

#     threading.Thread(target=ReceiveMessage, args=(client,), daemon=True).start()

#     while True:
#         try:
#             message = input("Client: ").strip()

#             if message:
#                 formatted = f"{username}: {message}"
#                 client.send(formatted.encode('utf-8'))
        
#         except KeyboardInterrupt:
#             print("\nExiting Chat!")
#             client.close()

#             break

# if __name__ == "__main__":
#     if len(sys.argv) < 2:
#         print("Usage: python Client.py <username>")
#     else:
#         StartChat(sys.argv[1])

import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def show_history(username):
    try:
        response = requests.get(f"{BASE_URL}/history/{username}")
        if response.status_code == 200:
            messages = response.json()
            for msg in messages:
                print(f"[{msg['m_time']}] {msg['sender']}: {msg['message']}")
        else:
            print("Could not retrieve history.")
    except Exception as e:
        print(f"Error fetching history: {e}")

def start_chat(username):
    print(f"Welcome, {username}! Starting chat with server.")
    show_history(username)

    while True:
        try:
            message = input("You: ").strip()
            if not message:
                continue

            payload = {
                "sender": username,
                "receiver": "server",
                "message": message
            }

            response = requests.post(f"{BASE_URL}/send", json=payload)

            if response.status_code == 200:
                print(f"Server: {response.json()['reply']}")
            else:
                print("Failed to send message.")

        except KeyboardInterrupt:
            print("\nExiting chat.")
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Client.py <username>")
    else:
        start_chat(sys.argv[1])