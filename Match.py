from datetime import datetime
from Team import Team
from Referee import Referee
from Player import Player
from LineUp import LineUp

class Match():
    def __init__(self, match_datetime: datetime, team_A: LineUp, team_B: LineUp):
        self.__match_datetime = match_datetime
        self.__team_A = team_A
        self.__team_B = team_B
        self.__score_team_A = 0
        self.__score_team_B = 0
        self.__match_referees = []


    @property
    def team_A(self) -> LineUp:
        return self.__team_A


    @property
    def team_B(self) -> LineUp:
        return self.__team_B


    def set_match_score(self, score_A, score_B):
        self.__score_team_A = score_A
        self.__score_team_B = score_B


    def add_referee(self, ref: Referee):
        self.__match_referees.append(ref)


    @property
    def match_referees(self):
        return self.__match_referees


    def add_player(self, player: Player, team: Team):
        if self.__team_A == team:
            self.__team_A_lineup.append(player)
        elif self.__team_B == team:
            self.__team_B_lineup.append(player)
        else:
            raise ValueError("Team is not in match")


    def is_upcoming(self):
        if self.__match_datetime > datetime.now():
            return True
        else:
            return False


    @property
    def match_datetime(self):
        return self.__match_datetime