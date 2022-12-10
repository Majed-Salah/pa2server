import re
from threading import Thread
import datetime
from socket import socket, AF_INET, SOCK_STREAM
from Server import Server
from Tournament.Tournament import Tournament


class ClientWorker(Thread):
    @property
    def connection(self):
        return self.__connection

    @property
    def socket(self):
        return self.__socket

    @property
    def keep_running_client(self):
        return self.__keep_running_client

    def __init__(self, client_socket, server: Server):
        super().__init__()
        self.__socket = client_socket
        self.__keep_running_client = True
        self.__server = server

    def run(self):
        while self.__keep_running_client:
            try:
                client_msg = self.__socket.recv(1024).decode('UTF-8')  # receive a line of instruction
                if client_msg == "T|":
                    self.__socket.send("0|OK".encode('UTF-8'))
                    # TODO server.removeCW(self)
                    break

                elif client_msg == "TERMINATE|":
                    self.__socket.close()  # TODO unsure if this is right
                    break

                else:
                    server_response = self.process_client_message(client_msg)
                    self.__socket.send(server_response.encode('UTF-8'))
            except:
                return "1|ERR"

    # -------------- EXAMPLE MESSAGES ---------------
    # [CLI]Sending>> C|USA
    # [CLI]Received>> 0|OK|Added Country

    # [CLI]Sending>> D|T1|USA
    # [CLI]Received>> 0|OK|Added team to tournament

    # [CLI]Sending>> C|A
    # [CLI]Received>> 0|OK|Added Country

    # [CLI]Sending>> R|R1|A
    # [CLI]Received>> 0|OK|Referee added to tournament

    def process_client_message(self, msg: str):
        # message = "D\n|T1\n|USA\n"
        clean_msg = ""
        for s in msg.split("|"):
            stripped_s = s.rstrip('\n')
            clean_msg += stripped_s + "|"
        clean_msg.split("|")
        print("HERE: " + clean_msg)

        t = self.__server.tournament
        split_msg = msg.split("|")
        command = split_msg[0]

        if command == "D":
            try:
                t.add_team(split_msg[1], split_msg[2])
                return "0|OK|Added team to tournament"
            except:
                return "1|ERR"

        if command == 'C':
            try:
                t.add_country(split_msg[1])
                print(t.participating_countries)
                return "0|OK|Added Country"
            except:
                return "1|ERR"

        if command == "R":
            try:
                t.add_referee(split_msg[1], split_msg[2])
                return "0|OK|Referee added to tournament"
            except:
                return "1|ERR"

        if command == "P":
            try:
                t.add_player(split_msg[1], split_msg[2], int(split_msg[3]), float(split_msg[4]), float(split_msg[5]))
                return "0|OK|Player added to tournament"
            except:
                return "1|ERR"

        if command == "M":
            try:
                t.add_match(datetime.datetime.strptime(split_msg[1], '%d/%m/%y'), split_msg[2], split_msg[3])
                return "0|OK|Successfully added match to tournament."
            except:
                return "1|ERR"

        if command == "A":
            try:
                print(f"CHECKING DATE FORMAT: ", datetime.datetime.strptime(split_msg[1], '%d/%m/%y'))
                t.add_referee_to_match(datetime.datetime.strptime(split_msg[1], '%d/%m/%y'), split_msg[2])
            except:
                return "1|ERR"

        if command == "Z":
            try:
                t.check_referee_for_match(datetime.datetime.strptime(split_msg[1], '%d/%m/%y'), split_msg[2])
            except:
                return "1|ERR"

        if command == "S":
            try:
                t.set_match_score(datetime.datetime.strptime(split_msg[1], '%d/%m/%y'), int(split_msg[2]),
                                  int(split_msg[3]))
                return "0|OK|Match score successfully set."
            except:
                return "1|ERR"

        if command == "L":
            try:
                t.get_upcoming_matches()
            except:
                return "1|ERR"

        if command == "G":
            try:
                response = "0|OK"
                matches = t.get_matches_on(datetime.datetime.strptime(split_msg[1], '%d/%m/%y'))
                for match in matches:
                    response += "|" + match.__str__()
                return response
            except:
                return "1|ERR"

        if command == "F":
            try:
                response = "0|OK"
                matches = t.get_matches_for(split_msg[1])
                for match in matches:
                    response += "|" + match.__str__()
                return response
            except:
                return "1|ERR|No matches for selected team."

        if command == "U":
            try:
                response = "0|OK"
                line_ups = t.get_match_lineups(datetime.datetime.strptime(split_msg[1], '%d/%m/%y'))
                for lineup in line_ups:
                    response += "|" + lineup.__str__()
                return response
            except:
                return "1|ERR"

        if command == "H":
            try:
                response = "0|OK"
                matches = t.list_matches()
                for match in matches:
                    response += "|" + match.match_datetime()
                return response
            except:
                return "1|ERR"

        if command == "HH":
            try:
                response = "0|OK"
                detailed_matches = t.list_matches()
                for match in detailed_matches:
                    if match.match_datetime() < datetime.datetime.now():
                        response += "|" + match.team_a().name() + "vs" + \
                                    match.team_b().name() + " @ " + match.match_datetime() + ", SCORE:" + match.get_match_score()
            except:
                return "1|ERR"

        if command == "W":
            try:
                response = "0|OK"
                teams = t.list_teams()
                for team in teams:
                    response += "|" + team.name
                return response
            except:
                return "1|ERR"

        if command == "Y":
            try:
                t.add_player_to_match(datetime.datetime.strptime(split_msg[1], '%d/%m/%y'), split_msg[2], split_msg[3])
                return "0|OK|Player added to match."
            except:
                return "1|ERR"

        if command == "T":
            try:
                self.__keep_running_client = False
            except:
                return "1|ERR"

        if command == "SS":
            try:
                # TODO SS Are we going to save things to a file?
                pass
            except:
                return "1|ERR"

        if command == "LS":
            try:
                # TODO LS Are we going to load things from a file?
                pass
            except:
                return "1|ERR"

        self.__socket.close()
        self.__keep_running_client = False
        self.__server.shutdown_server()

# test = ClientWorker()
# test.start()
