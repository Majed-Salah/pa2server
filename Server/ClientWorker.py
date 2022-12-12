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
                if client_msg == "T|" or client_msg == '|':
                    self.__socket.send("0|OK".encode('UTF-8'))
                    # TODO server.removeCW(self)
                    self.__keep_running_client = False
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

        t = self.__server.tournament

        clean_msg = msg.rstrip('\n')
        split_msg = clean_msg.split("|")
        command = split_msg[0]

        print("command:", command)

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
                t.add_match(datetime.datetime.strptime(split_msg[1], '%Y-%m-%dT%H:%M'), split_msg[2], split_msg[3])
                return "0|OK|Successfully added match to tournament.\n"
            except:
                return "1|ERR|Failed to add match to tournament.\n"

        if command == "A":
            try:
                t.add_referee_to_match(datetime.datetime.fromisoformat(split_msg[1]), split_msg[2])
            except:
                return "1|ERR|Could not add referee to match\n"

        if command == "Z":
            try:
                t.check_referee_for_match(datetime.datetime.fromisoformat(split_msg[1]), split_msg[2])
            except:
                return "1|ERR\n"

        if command == "S":
            try:
                t.set_match_score(datetime.datetime.fromisoformat(split_msg[1]), int(split_msg[2]),
                                  int(split_msg[3]))
                return "0|OK|Match score successfully set.\n"
            except Exception as e:
                return f"1|ERR|{e}\n"

        if command == "L":
            try:
                t.get_upcoming_matches()
            except:
                return "1|ERR\n"

        if command == "G":
            try:
                response = "0|OK"
                matches = t.get_matches_on(datetime.datetime.fromisoformat(split_msg[1]))
                for match in matches:
                    print(1)
                    response += f"|{match.__str__()}"
                print("resp:", response)
                return response + "\n"
            except Exception as e:
                return f"1|ERR|{e}\n"

        if command == "F":
            try:
                print("FFF w/", split_msg)
                response = "0|OK"
                matches = t.get_matches_for(split_msg[1])
                print("matches:", matches)
                for match in matches:
                    print("HEREHHD", match.__str__())
                    response += "|" + match.__str__()
                print("response:", response)
                return response + "\n"
            except Exception as e:
                return f"1|ERR|{e}\n"

        if command == "U":
            try:
                response = "0|OK"
                print(split_msg[1])
                print("start:", datetime.datetime.fromisoformat(split_msg[1]))
                line_ups = t.get_match_lineups(datetime.datetime.fromisoformat(split_msg[1]))
                for lineup in line_ups:
                    print("lineup.__str__():", lineup.__str__())
                    response += f"|{lineup.__str__()}"
                print("response:", response)
                return response + "\n"
            except Exception as e:
                return f"1|ERR|{e}\n"

        if command == "H":
            try:
                response = "0|OK"
                for match in t.list_matches:
                    response += f"|{match.match_datetime}"
                return response + "\n"
            except:
                return "1|ERR\n"

        if command == "HH":
            try:
                response = ""
                detailed_matches = t.list_matches
                for match in detailed_matches:
                    response += f"|{match.__str__()}"
                    # if match.match_datetime > datetime.datetime.now():
                    #     response = f"0|OK|{match.team_a.name} vs {match.team_b.name} @ {match.match_datetime}, SCORE: {match.get_match_score()}\n"
                return f"0|OK{response}\n"
            except:
                return "1|ERR|Could not retrieve matches on these filters.\n"

        if command == "W":
            try:
                response = "0|OK"
                for team in t.list_teams:
                    response += "|" + team.name
                return response + "\n"
            except:
                return "1|ERR|Failed to retrieve teams.\n"

        if command == "Y":
            try:
                t.add_player_to_match(datetime.datetime.fromisoformat(split_msg[1]), split_msg[2], split_msg[3])
                return "0|OK|Player added to match.\n"
            except Exception as e:
                return f"1|ERR|{e}\n"

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
