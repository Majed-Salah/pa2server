from socket import socket, AF_INET, SOCK_STREAM
from Tournament import Tournament
from threading import Thread
import ClientWorker

server_socket = socket()

server_socket.bind(('localhost', 6000))
server_socket.listen(5)

client_socket, addr = server_socket.accept()
print(f'Connected to: {addr}')

client_message = client_socket.recv(1024).decode('UTF-8')
print(client_message)

class Server(Thread):
    def __init__(self, ip, port, tournament_name):
        self.server_socket = socket()
        self.ip = ip
        self.port = port
        self.tournament = Tournament(tournament_name)
        self.client_workers = []
        self.keep_server_running = True
        super().__init__()

    def bind(self):
        server_socket.bind((self.ip, self.port))

    def accept(self) -> tuple:
        self.bind()
        self.server_socket.listen(5)
        server_socket.accept()

    def run(self):
        while self.keep_server_running:

            client_socket, addr = self.accept()

            new_client_worker = ClientWorker(self, client_socket)
            self.client_workers.append(new_client_worker)
            new_client_worker.start()


    def shutdown_client_worker(self, client_worker):
        client_worker.close()