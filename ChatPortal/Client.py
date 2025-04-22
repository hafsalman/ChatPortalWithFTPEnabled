import socket
import threading
import sys

# Accept the username from command-line args
if len(sys.argv) < 2:
    print("Username is required as an argument.")
    sys.exit(1)

username = sys.argv[1]

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client_socket.connect((SERVER_HOST, SERVER_PORT))
except Exception as e:
    print(f"❌ Connection failed: {e}")
    sys.exit()

# Send username to server on connection
client_socket.send(username.encode('utf-8'))

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(4096).decode('utf-8')
            if not message:
                print("🔌 Disconnected from server.")
                break
            print(message)
        except Exception as e:
            print(f"⚠️ Error receiving message: {e}")
            break

def send_messages(sock):
    while True:
        try:
            msg = input()
            if msg.strip().lower() == "exit":
                print("🔚 Exiting chat.")
                sock.close()
                break
            sock.send(msg.encode('utf-8'))
        except Exception as e:
            print(f"⚠️ Error sending message: {e}")
            break

# Start receiving thread
recv_thread = threading.Thread(target=receive_messages, args=(client_socket,))
recv_thread.daemon = True
recv_thread.start()

# Start sending loop
send_messages(client_socket)
