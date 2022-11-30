from datetime import datetime
from Country import Country
from Team import Team
from Match import Match
from Referee import Referee

class Tournament():
    def __init__(self, name: str, start_date: datetime, end_date: datetime):
        self.__name = name
        self.__start_date = start_date
        self.__end_date = end_date
        self.__participating_countries = []
        self.__list_teams = []
        self.__list_referees = []
        self.__list_matches = []


    def load_from_file(self):
        pass


    def save_to_file(self):
        pass


    def add_country(self, country_name: str):
        matching_countries = [country for country in self.__participating_countries if country.country_name == country_name]

        if len(matching_countries) == 0:
            country = Country(country_name)
            self.__participating_countries.append(country)

        else:
            raise ValueError("Country already in tournament")


    def add_team(self, team_name: Team, country_name: str):
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


    def add_match(self, match_datetime: datetime, team_A_name: str, team_B_name:str):
        team_A = None
        team_B = None

        team_A_list = [team for team in self.__list_teams if team.name == team_A_name]
        team_B_list = [team for team in self.__list_teams if team.name == team_B_name]

        if len(team_A_list) == 1:
            team_A = team_A_list[0]
        if len(team_B_list) == 1:
            team_B = team_B_list[0]


        if team_A is None or team_B is None:
            raise ValueError("Team is not participating in the tournament.")

        match = Match(match_datetime, team_A, team_B)
        self.__list_matches.append(match)


    def add_referee_to_match(self, match_datetime: datetime, ref_name: str):
        match: Match = None
        ref: Referee = None

        list_matches = [match for match in self.__list_matches if match.match_datetime == match_datetime]

        if len(list_matches) == 0:
            raise ValueError("Match is not in tournament.")
        elif len(list_matches) == 1:
            match = list_matches[0]

        list_refs = [ref for ref in self.__list_referees if ref.name == ref_name]

        if len(list_refs) == 0:
            raise ValueError("No referee with matching name.")
        elif len(list_refs) == 1:
            ref = list_refs[0]

        match.add_referee(ref)