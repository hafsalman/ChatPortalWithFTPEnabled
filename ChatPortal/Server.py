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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB_Connection.Connection import createConnection

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LOCALHOST = '127.0.0.1'
port = 5555

server_socket.bind((LOCALHOST, port))
server_socket.listen(1)

print("Server running on ", port)

client_socket, addr = server_socket.accept()

username = client_socket.recv(1024).decode()
print(f"{username} connected from {addr}")

while True:
    msg_received = client_socket.recv(1024).decode()
    
    if not msg_received:
        break

    print(f"{username}: {msg_received}")
    save_message(username, 'server', msg_received)

    msg_send = input("Me: ")
    client_socket.send(msg_send.encode('utf-8'))
    save_message('server', username, msg_send)

client_socket.close()

def save_message(sender, receiver, message):
    conn = createConnection()
    if conn is None:
        print("DB Connection Failed!")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO MESSAGES (sender, receiver, message)
            VALUES (%s, %s, %s)
        """, (sender, receiver, message))
        conn.commit()
    except Exception as e:
        print(f"Failed to save message: {e}")
    finally:
        cursor.close()
        conn.close()