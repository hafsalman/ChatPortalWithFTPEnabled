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

def SaveMessage (sender, receiver, message):
    conn = createConnection()

    if conn is None:
        print("Failed to save messaged!")
        return
    
    try:
        cursor = conn.cursor
        cursor.execute("""INSERT INTO MESSAGES (sender, receiver, message) VALUES (%s, %s, %s)""", (sender, receiver, message))
        conn.commit()

    except Exception as e:
        print(f"Failed to save in DB!")

    finally:
        cursor.close()
        conn.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LOCALHOST = '127.0.0.1'
PORT = 5555

server_socket.bind((LOCALHOST, PORT))
server_socket.listen(1)
print(f"Server has started on {LOCALHOST}: {PORT}")

client_socket, addr = server_socket.accept()
print(f"Connection from {addr}")

username = client_socket.recv(1024).decode().strip()
print(f"{username} connected!")

while True:
    try:
        r_message = client_socket.recv(1024).decode().strip()

        if not r_message:
            print("Connection closed by client!")
            break

        print(f"{username}: {r_message}")
        SaveMessage(username, 'server', r_message)

        sendMessage = input("Me: ").strip()

        if sendMessage:
            client_socket.send(sendMessage.encode('utf-8'))
            SaveMessage('server', username, sendMessage)

    except Exception as e:
        print(f"Error: {e}")
        break

client_socket.close()
print("{username} disconnected")