from socket import socket, AF_INET, SOCK_STREAM

host = "127.0.0.1"
port = 6000

a_socket = socket(AF_INET, SOCK_STREAM)
a_socket.connect((host, port))

message = "Howdy".encode('UTF-8')
a_socket.send(message)