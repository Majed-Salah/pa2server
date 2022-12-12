from threading import Thread
import datetime
from Server import Server
import pickle


class ClientWorker(Thread):
    @property
    def socket(self):
        return self.__socket

    @property
    def server(self):
        return self.__server

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
                    print("Server response test")
                    server_response = self.process_client_message(client_msg)
                    self.__socket.send(server_response.encode('UTF-8'))
            except:
                return "1|ERR"


    def process_client_message(self, msg: str):
        msg.replace("\n", "")

        clean_msg = ""
        for s in msg.split("|"):
            stripped_s = s.rstrip('\n')
            clean_msg += stripped_s + "|"

        clean_msg.split("|")
        print("HERE: " + clean_msg)

        t = self.__server.tournament
        split_msg = msg.split("|")
        command = split_msg[0]




        # print(command, split_msg[1])

        if command == "D":
            try:
                t.add_team(split_msg[1], split_msg[2])
                return "0|OK|Added team to tournament\n"
            except:
                return "1|ERR|Could not add team to tournament.\n"

        if command == 'C':
            try:
                t.add_country(split_msg[1])
                print(t.participating_countries)
                return "0|OK|Added Country\n"
            except:
                return "1|ERR|Country already in tournament.\n"

        if command == "R":
            try:
                t.add_referee(split_msg[1], split_msg[2])
                return "0|OK|Referee added to tournament.\n"
            except:
                return "1|ERR|Failed to add referee to tournament.\n"

        if command == "P":
            try:
                t.add_player(split_msg[1], split_msg[2], int(split_msg[3]), float(split_msg[4]), float(split_msg[5]))
                return "0|OK|Player added to tournament.\n"
            except:
                return "1|ERR|Failed to add player to team.\n"

        if command == "M":
            try:
                print(f"TEST FORMAT: {datetime.datetime.strptime(split_msg[1], '%Y-%m-%dT%H:%M')} -> Type({type(datetime.datetime.strptime(split_msg[1], '%Y-%m-%dT%H:%M'))})")
                print("----")
                print(fr'{split_msg[2]}')
                print(fr'{split_msg[3]}')
                t.add_match(datetime.datetime.strptime(split_msg[1], '%Y-%m-%dT%H:%M'), split_msg[2], split_msg[3])
                return "0|OK|Successfully added match to tournament.\n"
            except:
                return "1|ERR|Failed to add match to tournament.\n"

        if command == "A":
            try:
                print(f"CHECKING DATE FORMAT: ", datetime.datetime.strptime(split_msg[1], '%d/%m/%y'))
                t.add_referee_to_match(datetime.datetime.strptime(split_msg[1], '%d/%m/%y'), split_msg[2])
            except:
                return "1|ERR\n"

        if command == "Z":
            try:
                t.check_referee_for_match(datetime.datetime.strptime(split_msg[1], '%d/%m/%y'), split_msg[2])
            except:
                return "1|ERR\n"

        if command == "S":
            try:
                t.set_match_score(datetime.datetime.strptime(split_msg[1], '%d/%m/%y'), int(split_msg[2]),
                                  int(split_msg[3]))
                return "0|OK|Match score successfully set.\n"
            except:
                return "1|ERR\n"

        if command == "L":
            try:
                t.get_upcoming_matches()
            except:
                return "1|ERR\n"

        if command == "G":
            try:
                response = "0|OK\n"
                matches = t.get_matches_on(datetime.datetime.strptime(split_msg[1], '%d/%m/%y'))
                for match in matches:
                    response += "|" + match.__str__()
                return response
            except:
                return "1|ERR\n"

        if command == "F":
            try:
                response = "0|OK\n"
                matches = t.get_matches_for(split_msg[1])
                for match in matches:
                    response += "|" + match.__str__()
                return response
            except:
                return "1|ERR|No matches for selected team.\n"

        if command == "U":
            try:
                response = "0|OK\n"
                line_ups = t.get_match_lineups(datetime.datetime.strptime(split_msg[1], '%d/%m/%y'))
                for lineup in line_ups:
                    response += "|" + lineup.__str__()
                return response
            except:
                return "1|ERR\n"

        if command == "H":
            try:
                response = "0|OK\n"
                matches = t.list_matches()
                for match in matches:
                    response += "|" + match.match_datetime()
                return response
            except:
                return "1|ERR\n"

        if command == "HH":
            try:
                response = "0|OK"
                detailed_matches = t.list_matches
                for match in detailed_matches:
                    if match.match_datetime < datetime.datetime.now():
                        response += "|" + match.team_a.name + "vs" + \
                                    match.team_b.name + " @ " + match.match_datetime + ", SCORE:" + match.get_match_score
                response += "\n"
                print(f"RESPONSE: {response}")
            except:
                return "1|ERR\n"

        if command == "W":
            try:
                response = "0|OK"
                # resp = "0|OK|T1|T2\n"
                # return resp
                print(f"RESPONSE 1: {response}")
                for team in t.list_teams:
                    response += "|" + team.name
                    print(f"RESPONSE 2: '{response}'")
                print(f"RESPONSE 3: '{response}'")

                return response + "\n"
            except:
                return "1|ERR\n"

        if command == "Y":
            try:
                t.add_player_to_match(datetime.datetime.strptime(split_msg[1], '%d/%m/%y'), split_msg[2], split_msg[3])
                return "0|OK|Player added to match.\n"
            except:
                return "1|ERR\n"

        if command == "T":
            try:
                self.__keep_running_client = False
            except:
                return "1|ERR\n"

        if command == "SS":
            try:
                pickle_out = open("./tournament.pickle", "wb")
                pickle.dump(t, pickle_out)
                pickle_out.close()
                return "0|OK|State Saved Successfully.\n"
            except:
                return "1|ERR|Could not save state to file.\n"

        if command == "LS":
            try:
                pickle_in = open("./tournament.pickle", "rb")
                t = pickle.load(pickle_in)
                pickle_in.close()
                self.server.set_tournament(t)
                return "0|OK|Successfully loaded serialized file.\n"
            except:
                return "1|ERR|Could not load state from file.\n"

        # self.__socket.close()
        # self.__keep_running_client = False
        # self.__server.shutdown_server()

# test = ClientWorker()
# test.start()
