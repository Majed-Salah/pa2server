import socket as sckt
from socket import socket, AF_INET, SOCK_STREAM

host = "127.0.0.1"
port = 50000

a_socket = socket(AF_INET, SOCK_STREAM)
a_socket

message = "Howdy".encode('UTF-8')
a_socket.send(message)