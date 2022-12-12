from datetime import datetime
from Team import Team
from Referee import Referee
from Player import Player
from LineUp import LineUp


class Match:
    def __init__(self, match_datetime: datetime, team_a: Team, team_b: Team):
        self.__match_datetime = match_datetime
        self.__team_a = team_a
        self.__team_b = team_b
        self.__team_a_lineup = LineUp(team_a)
        self.__team_b_lineup = LineUp(team_b)
        self.__score_team_A = 0
        self.__score_team_B = 0
        self.__match_referees = []

    def __str__(self):
        return str(self.__match_datetime) + " -- " + self.team_a.name + " AGAINST " + self.team_b.name

    @property
    def team_a(self) -> Team:
        return self.__team_a

    @property
    def team_b(self) -> Team:
        return self.__team_b

    @property
    def team_a_lineup(self) -> LineUp:
        return self.__team_a_lineup

    @property
    def team_b_lineup(self) -> LineUp:
        return self.__team_b_lineup

    @property
    def score_team_a(self):
        return self.__score_team_A

    @property
    def score_team_b(self):
        return self.__score_team_B

    @property
    def match_datetime(self):
        return self.__match_datetime

    @property
    def match_referees(self):
        return self.__match_referees

    def add_referee(self, ref: Referee):
        self.__match_referees.append(ref)

    def add_player_to_lineup(self, player: Player, team: Team):
        # Add the player passed in, to the squad of team that was passed in (team_a or team_b)
        if self.__team_a == team:
            self.__team_a_lineup.add_player(player)
        elif self.__team_b == team:
            self.__team_b_lineup.add_player(player)
        else:
            raise ValueError("Team is not in match")

    def set_match_score(self, score_a, score_b):
        self.__score_team_A = score_a
        self.__score_team_B = score_b

    def get_match_score(self) -> str:
        return " (" + str(self.score_team_a) + " - " + str(self.score_team_b) + ")"

    def is_upcoming(self):
        if self.__match_datetime > datetime.now():
            return True
        else:
            return False