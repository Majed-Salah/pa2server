from socket import socket, AF_INET, SOCK_STREAM

host = "127.0.0.1"
port = 10000

a_socket = socket(AF_INET, SOCK_STREAM)
a_socket.connect((host, port))

message = "C|USA".encode('UTF-8')
a_socket.send(message)