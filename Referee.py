from Country import Country

class Referee():
    def __init__(self, name: str, country: Country):
        self.__name = name
        self.__country = country


    @property
    def country(self):
        return self.__country


    @property
    def name(self):
        return self.__name