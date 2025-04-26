# import socket
# server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# LOCALHOST = '127.0.0.1'
# port = 9997

# server_socket.bind((LOCALHOST,port))
# server_socket.listen(5)

# print("Server started...")

# client_sockets,addr=server_socket.accept()
# while True:
#     msg_received = client_sockets.recv(1024)
#     msg_received = msg_received.decode()
#     print("Client:", msg_received)
    
#     msg_send = input("Me:")
#     client_sockets.send(msg_send.encode('UTF-8'))

# client_sockets.close()
 
import socket
import mysql.connector
from datetime import datetime
import os
import sys

# Add DB connection path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB_Connection.Connection import createConnection

# === Save Message to DB ===
def save_message(sender, receiver, message):
    conn = createConnection()
    if conn is None:
        print("❌ DB connection failed while saving message.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO MESSAGES (sender, receiver, message)
            VALUES (%s, %s, %s)
        """, (sender, receiver, message))
        conn.commit()
    except Exception as e:
        print(f"❌ Failed to save message: {e}")
    finally:
        cursor.close()
        conn.close()

# === Server Setup ===
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LOCALHOST = '127.0.0.1'
PORT = 5555

server_socket.bind((LOCALHOST, PORT))
server_socket.listen(1)
print(f"✅ Server started on {LOCALHOST}:{PORT}")

client_socket, addr = server_socket.accept()
print(f"📥 Connection accepted from {addr}")

# Receive client username
username = client_socket.recv(1024).decode().strip()
print(f"👤 {username} connected")

# === Chat Loop ===
while True:
    try:
        msg_received = client_socket.recv(1024).decode().strip()
        if not msg_received:
            print("❌ Connection closed by client.")
            break

        print(f"{username}: {msg_received}")
        save_message(username, 'server', msg_received)

        msg_send = input("Me: ").strip()
        if msg_send:
            client_socket.send(msg_send.encode('utf-8'))
            save_message('server', username, msg_send)

    except Exception as e:
        print(f"❌ Error in communication: {e}")
        break

client_socket.close()
print("🔌 Client disconnected")