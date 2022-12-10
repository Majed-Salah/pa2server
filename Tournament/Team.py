from Country import Country
from Player import Player


class Team:
    def __init__(self, name: str, country: Country):
        self.__name = name
        self.__country = country
        self.__squad = []

    @property
    def country(self):
        return self.__country

    @property
    def name(self):
        return self.__name

    @property
    def squad(self) -> list:
        return self.__squad

    def add_player(self, player_name: str, age: int, height: float, weight: float):
        player = Player(player_name, age, height, weight)
        self.__squad.append(player)
