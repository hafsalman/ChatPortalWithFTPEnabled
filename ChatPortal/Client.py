import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
LOCALHOST = '127.0.0.1'
port = 9997

s.connect((LOCALHOST,port))
print("New client created:")

while True:
    client_message = input("Me: ")
    s.send(client_message.encode())

    msg_received = s.recv(1024)
    msg_received = msg_received.decode()
    print("Server:",msg_received)

    if msg_received == 'exit':
        break
s.close()