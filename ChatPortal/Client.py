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
import threading
import sys
import os
import mysql.connector
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB_Connection.Connection import createConnection

HOST = '127.0.0.1'
PORT = 5555

def show_history(username):
    conn = createConnection()
    if conn is None:
        print("Couldn't connect to the Database!")
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT sender, receiver, message, m_time 
            FROM MESSAGES 
            WHERE (sender = %s AND receiver = 'server') 
               OR (sender = 'server' AND receiver = %s)
            ORDER BY m_time ASC
        """, (username, username))

        history = cursor.fetchall()

        if history:
            print("\n--- Chat History ---")
            for sender, receiver, message, timestamp in history:
                timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{timestamp_str}] {sender}: {message}")
            print("--- End of History ---\n")
        else:
            print("No chat history found.\n")

    except mysql.connector.Error as e:
        print(f"Database error: {e}")

    finally:
        cursor.close()
        conn.close()

def receive_message(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')

            if message:
                print(f"\n{message}\nClient: ", end="", flush=True)
            else:
                print("\nServer disconnected.")
                break

        except Exception as e:
            print(f"Connection lost: {e}")
            break

def start_chat(username):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        client.send(username.encode('utf-8'))
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # Show previous chat history
    show_history(username)

    threading.Thread(target=receive_message, args=(client,), daemon=True).start()

    while True:
        try:
            message = input("Client: ").strip()

            if message:
                formatted_message = f"{username}: {message}"
                client.send(formatted_message.encode('utf-8'))

        except KeyboardInterrupt:
            print("\nExiting Chat...")
            client.close()
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python Client.py <username>")
    else:
        start_chat(sys.argv[1])