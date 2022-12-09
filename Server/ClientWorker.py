from threading import Thread


class ClientWorker(Thread):

    def __init__(self, server, connection):
        self.__connection = connection
        self.__server = server
        self.__keepRunningClient = True
        super().__init__()

    @property
    def connection(self):
        return self.__connection

    @property
    def server(self):
        return self.__server

    @property
    def keepRunningClient(self):
        return self.__keepRunningClient

    def run(self):

        while self.__keepRunningClient:
            parse_message()

        pass
        # while (self.__keepRunningClient){
        #
        # }


    def close(self):
        self.__keepRunningClient = False