from datetime import datetime
from Team import Team
from Country import Country
from Match import Match
from Referee import Referee
from Player import Player
from LineUp import LineUp


class Tournament:
    def __init__(self, name: str, start_date: datetime.date, end_date: datetime.date):
        self.__name = name
        self.__start_date = start_date
        self.__end_date = end_date
        self.__participating_countries = []
        self.__list_teams = []
        self.__list_referees = []
        self.__list_matches = []

    @property
    def list_matches(self):
        return self.__list_matches

    @property
    def list_teams(self):
        return self.__list_teams

    @property
    def list_referees(self):
        return self.__list_referees

    @property
    def participating_countries(self):
        return self.__participating_countries

    def load_from_file(self):
        pass

    def save_to_file(self):
        pass

    def add_country(self, country_name: str):
        matching_countries = [country for country in self.__participating_countries if
                              country.country_name == country_name]

        if len(matching_countries) == 0:
            country = Country(country_name)
            self.__participating_countries.append(country)

        else:
            raise ValueError("Country already in tournament")

    def add_team(self, team_name: str, country_name: str):
        country = None

        for c in self.__participating_countries:
            if c.country_name == country_name:
                country = c

        if not country:
            raise ValueError("Country is not participating in world cup")

        team = Team(team_name, country)
        self.__list_teams.append(team)

    def add_referee(self, ref_name: str, country_name: str):
        country = None

        for c in self.__participating_countries:
            if c.country_name == country_name:
                country = c

        if not country:
            raise ValueError("Country is not participating in world cup")

        referee = Referee(ref_name, country)
        self.__list_referees.append(referee)

    def add_player(self, team_name: str, player_name: str, age: int, height: float, weight: float):
        list_teams = [team for team in self.__list_teams if team.name == team_name]
        team = None

        if len(list_teams) == 1:
            team = list_teams[0]

        team.add_player(player_name, age, height, weight)

    def add_match(self, match_datetime: datetime, team_A_name: str, team_B_name: str):
        team_A = None
        team_B = None

        team_A_list = [team for team in self.list_teams if team.name == team_A_name]
        team_B_list = [team for team in self.list_teams if team.name == team_B_name]

        if len(team_A_list) == 1:
            team_A = team_A_list[0]
        if len(team_B_list) == 1:
            team_B = team_B_list[0]

        if team_A is None or team_B is None:
            raise ValueError("Team is not participating in the tournament.")

        match = Match(match_datetime, team_A, team_B)
        self.list_matches.append(match)

    def add_referee_to_match(self, match_datetime: datetime, ref_name: str):
        match: Match = None
        ref: Referee = None

        # return list of matches where the passed datetime is equal to match datetime
        list_matches = [match for match in self.__list_matches if match.match_datetime == match_datetime]

        if len(list_matches) == 0:
            raise ValueError("Match is not in tournament.")
        elif len(list_matches) == 1:
            match = list_matches[0]

        # check if referee to be added in match is in list of tournament referees
        list_refs = [ref for ref in self.__list_referees if ref.name == ref_name]

        if len(list_refs) == 0:  # meaning that referee with passed name is not in tournament
            raise ValueError("No referee with matching name.")
        elif len(list_refs) == 1: # will return list of size 1 if referee in tournament (cant have multiple with same name)
            ref = list_refs[0]

        match.add_referee(ref)

    def check_referee_for_match(self, match_datetime: datetime, ref_name: str) -> bool:
        match: Match = None
        ref: Referee = None

        list_matches = [match for match in self.__list_matches if match.match_datetime == match_datetime]

        if len(list_matches) == 0:
            return False
        elif len(list_matches) == 1:
            match = list_matches[0]

        list_refs = [ref for ref in self.__list_referees if ref.name == ref_name]

        if len(list_refs) == 0:
            return False
        elif len(list_refs) == 1:
            ref = list_refs[0]

        teama_country = match.team_A.team.country
        teamb_country = match.team_B.team.country

        if ref.country == teama_country or ref.country == teamb_country:
            return False

        return True

    def add_player_to_match(self, match_datetime: datetime, team_name: str, player_name: str):

        match: Match = None
        lineup: LineUp = None
        p: Player = None

        list_matches = [match for match in self.__list_matches if match.match_datetime == match_datetime]

        if len(list_matches) == 0:
            raise ValueError("Match is not in tournament.")
        elif len(list_matches) == 1:
            match = list_matches[0]

        if match.team_A.name == team_name:
            lineup = match.team_A
        elif match.team_B.name == team_name:
            lineup = match.team_B
        else:
            raise ValueError("Team not participating in this match")

        player_names = [player for player in lineup.team.squad]
        for player in player_names:
            if player.name == player_name:
                p = player

        lineup.add_player(p)

    def set_match_score(self, match_datetime: datetime, score_a: int, score_b: int):
        for match in self.__list_matches:
            if match.match_datetime() == match_datetime:
                match.set_match_score(score_a, score_b)  # found the right match

    def get_upcoming_matches(self) -> []:
        upcoming_matches = []
        for match in self.__list_matches:
            if match.is_upcoming():
                upcoming_matches.append(match)
        return upcoming_matches

    def get_matches_on(self, match_datetime: datetime):
        date_matches = []
        for match in self.__list_matches:
            if match.match_datetime == match_datetime:
                date_matches.append(match)
        return date_matches

    def get_matches_for(self, team_name: str):
        team_matches = []
        for match in self.list_matches:
            print(f"GMF: {match.team_a.name} == {team_name}")
            if match.team_a.name == team_name:
                team_matches.append(match)
        return team_matches

    def get_match_lineups(self, match_datetime: datetime):
        match_line_up = []
        for match in self.__list_matches:
            if match.match_datetime == match_datetime:
                match_line_up.append(match.__team_a_lineup)
                match_line_up.append(match.__team_b_lineup)

