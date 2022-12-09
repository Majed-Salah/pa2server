from socket import socket, AF_INET, SOCK_STREAM

server_socket = socket()

server_socket.bind(('localhost', 6000))
server_socket.listen(5)

client_socket, addr = server_socket.accept()
print(f'Connected to: {addr}')

client_message = client_socket.recv(1024).decode('UTF-8')
print(client_message)