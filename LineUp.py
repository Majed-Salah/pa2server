from Team import Team
from Player import Player

class LineUp():
    def __init__(self, team: Team):
        self.__team = team
        self.__listOfPlayers = []
        
        
    @property
    def team(self):
        return self.__team
    
    
    @property
    def list_of_players(self):
        return self.__listOfPlayers


    def add_player(self, player: Player):
        self.__listOfPlayers.append(player)