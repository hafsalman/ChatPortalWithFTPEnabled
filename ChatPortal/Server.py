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
import threading
import mysql.connector
from datetime import datetime
import os
import sys

# === DB Connection ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB_Connection.Connection import createConnection

# === Configuration ===
HOST = '127.0.0.1'
PORT = 5555

# === Broadcast / Respond to Client ===
def handle_client(client_socket, addr, username):
    print(f"✅ {username} connected from {addr}")

    while True:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            sender, receiver, message = data.split("|", 2)

            # Save to database
            save_message(sender, receiver, message)

            # Print to server console
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"[{timestamp}] {sender} -> {receiver}: {message}")

            # Respond back
            response = f"[{timestamp}] server: Message received ✔️"
            client_socket.send(response.encode('utf-8'))

            # Optionally, respond with actual messages here

        except Exception as e:
            print(f"❌ Error with {username}: {e}")
            break

    print(f"❌ {username} disconnected")
    client_socket.close()

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

# === Main Server Loop ===
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"🚀 Server running on {HOST}:{PORT}... Waiting for connections.")

    while True:
        client_socket, addr = server.accept()
        username = client_socket.recv(1024).decode('utf-8')  # Receive the username first

        # Start a new thread per client
        thread = threading.Thread(target=handle_client, args=(client_socket, addr, username))
        thread.start()

if __name__ == "__main__":
    start_server()