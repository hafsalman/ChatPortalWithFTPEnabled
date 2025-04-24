# import socket
# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# LOCALHOST = '127.0.0.1'
# port = 9997

# s.connect((LOCALHOST,port))
# print("New client created:")

# while True:
#     client_message = input("Me: ")
#     s.send(client_message.encode())

#     msg_received = s.recv(1024)
#     msg_received = msg_received.decode()
#     print("Server:",msg_received)

#     if msg_received == 'exit':
#         break
# s.close()

import socket
import threading
import sys
import os
import mysql.connector
from datetime import datetime

# === DB Connection ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB_Connection.Connection import createConnection

# === Configuration ===
HOST = '127.0.0.1'
PORT = 5555

# === Load Message History ===
def load_history(username):
    conn = createConnection()
    if conn is None:
        print("❌ Could not connect to DB for history.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sender, receiver, message, m_time
            FROM MESSAGES
            WHERE (sender = %s AND receiver = 'server') OR (sender = 'server' AND receiver = %s)
            ORDER BY m_time ASC
        """, (username, username))

        print("\n📜 Message History with Server:")
        print("-----------------------------------")
        for row in cursor.fetchall():
            sender, receiver, message, timestamp = row
            print(f"[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {sender}: {message}")

        print("-----------------------------------\n")

    except Exception as e:
        print("❌ Error loading history:", e)
    finally:
        cursor.close()
        conn.close()

# === Receive Messages ===
def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message:
                print(f"\n{message}\nClient: ", end="", flush=True)
            else:
                break
        except:
            print("\n❌ Connection lost.")
            break

# === Main Chat Function ===
def start_chat(username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return

    # Send your username to the server
    client.send(username.encode('utf-8'))

    # Load old messages
    load_history(username)

    print("💬 You are now chatting with the server.")
    print("Type your message and press Enter.\n")

    # Start receiving messages
    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    # Start sending messages
    while True:
        try:
            message = input("Client: ").strip()
            if message:
                formatted = f"{username}|server|{message}"
                client.send(formatted.encode('utf-8'))
        except KeyboardInterrupt:
            print("\n❌ Exiting chat.")
            client.close()
            break

# === Entry Point ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Client.py <username>")
    else:
        start_chat(sys.argv[1])


