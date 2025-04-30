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

import socket
import sys

def start_client():
    # Server details
    host = '127.0.0.1'
    port = 8000

    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # Send a welcome message or any data if needed
        client_socket.sendall(b'Hello, Server! Client is connected.')

        # Receive server response
        response = client_socket.recv(1024)
        print(f"Server response: {response.decode()}")

        # Keep the connection open and handle communication
        while True:
            message = input("Enter message to send to server (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024)
            print(f"Server response: {response.decode()}")

    except ConnectionRefusedError:
        print("Could not connect to the server. Make sure the server is running.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print("Connection closed.")

if __name__ == "__main__":
    start_client()