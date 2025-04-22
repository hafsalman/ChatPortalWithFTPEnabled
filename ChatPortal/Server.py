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
import datetime
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from DB_Connection.Connection import createConnection

HOST = '0.0.0.0'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}  # username -> socket

print(f"📡 Server listening on {HOST}:{PORT}")

def handle_client(client_socket, addr, username):
    print(f"✅ {username} connected from {addr}")
    clients[username] = client_socket

    # Send chat history
    send_chat_history(client_socket, username)

    while True:
        try:
            msg = client_socket.recv(4096).decode('utf-8')
            if not msg:
                break

            # Check for private message (e.g., @john Hello)
            if msg.startswith('@'):
                parts = msg.split(' ', 1)
                if len(parts) < 2:
                    continue
                target_username = parts[0][1:]
                actual_msg = parts[1]

                store_message(username, target_username, actual_msg)
                send_private_message(username, target_username, actual_msg)
            else:
                # Broadcast to everyone else
                for user, sock in clients.items():
                    if sock != client_socket:
                        try:
                            sock.send(f"[{username}]: {msg}".encode('utf-8'))
                        except:
                            pass
        except:
            break

    # Disconnecting
    print(f"❌ {username} disconnected.")
    del clients[username]
    client_socket.close()

def send_chat_history(client_socket, username):
    conn = createConnection()
    if not conn:
        return
    cursor = conn.cursor()

    try:
        query = """
            SELECT sender, receiver, message, m_time FROM MESSAGES 
            WHERE sender = %s OR receiver = %s
            ORDER BY m_time ASC
        """
        cursor.execute(query, (username, username))
        messages = cursor.fetchall()

        if messages:
            client_socket.send("🕘 Chat History:\n".encode('utf-8'))
            for sender, receiver, msg, m_time in messages:
                if receiver == username:
                    formatted = f"[{m_time}] {sender} ➜ You: {msg}"
                else:
                    formatted = f"[{m_time}] You ➜ {receiver}: {msg}"
                client_socket.send(formatted.encode('utf-8'))
    except Exception as e:
        print(f"⚠️ History error: {e}")
    finally:
        cursor.close()
        conn.close()

def store_message(sender, receiver, msg):
    conn = createConnection()
    if not conn:
        return
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO MESSAGES (sender, receiver, message)
            VALUES (%s, %s, %s)
        """, (sender, receiver, msg))
        conn.commit()
    except Exception as e:
        print(f"⚠️ Store error: {e}")
    finally:
        cursor.close()
        conn.close()

def send_private_message(sender, receiver, msg):
    if receiver in clients:
        try:
            clients[receiver].send(f"[Private] {sender} ➜ You: {msg}".encode('utf-8'))
            clients[sender].send(f"[Private] You ➜ {receiver}: {msg}".encode('utf-8'))
        except:
            pass
    else:
        clients[sender].send(f"⚠️ User {receiver} is not online.".encode('utf-8'))

def accept_connections():
    while True:
        client_socket, addr = server.accept()
        username = client_socket.recv(1024).decode('utf-8')
        threading.Thread(target=handle_client, args=(client_socket, addr, username), daemon=True).start()

accept_connections()