class Country():
    def __init__(self, name: str):
        self.__country_name = name

    @property
    def country_name(self):
        return self.__country_name
