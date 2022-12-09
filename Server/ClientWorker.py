from threading import Thread


class ClientWorker(Thread):

    def __init__(self):
        self.__connection = connection
        self.__server = server
        self.__keepRunningClient = True

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
        pass
        # while (self.__keepRunningClient){
        #
        # }