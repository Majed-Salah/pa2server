import datetime
from socket import socket, AF_INET, SOCK_STREAM
from Tournament import Tournament
from threading import Thread
import ClientWorker


# server_socket = socket()
#
# server_socket.bind(('localhost', 6000))
# server_socket.listen(5)
#
# client_socket, addr = server_socket.accept()
# print(f'Connected to: {addr}')
#
# client_message = client_socket.recv(1024).decode('UTF-8')
# print(client_message)


class Server(Thread):
    def __init__(self, ip, port, tournament_name):
        super().__init__()
        # 1. create a socket
        self.server_socket = socket()
        # 2. read in ip and port from Server instance for bind
        self.ip = ip
        self.port = port
        self.__tournament = Tournament.Tournament(tournament_name, datetime.date(2022, 1, 1), datetime.date(2022, 12, 30))
        self.client_workers = []
        self.keep_server_running = True
        self.bind_con()

    def bind_con(self):
        # 3. bind the server_socket
        self.server_socket.bind((self.ip, self.port))  # self.bind_con()

        # 4. listen for connections
        print("Listening for connections...")
        self.server_socket.listen(5)


    def accept_con(self) -> tuple:
        # 5. accept incoming connection
        client_socket, addr = self.server_socket.accept()
        print(f"Connected to : {addr}")
        return client_socket, addr

    @property
    def tournament(self):
        return self.__tournament

    def set_tournament(self, tourney: Tournament):
        self.__tournament = tourney

    def run(self):
        while self.keep_server_running:
            client_socket, addr = self.accept_con()
            # print(f"cs: {client_socket}\naddr: {addr}")

            new_client_worker = ClientWorker.ClientWorker(client_socket, self)
            self.client_workers.append(new_client_worker)
            new_client_worker.start()


    def shutdown_client_worker(self, client_worker):
        client_worker.close()


    def shutdown_server(self):
        self.server_socket.close()


if __name__ == '__main__':
    s = Server('localhost', 10000, "FIFA 2022 QATAR")
    s.start()
