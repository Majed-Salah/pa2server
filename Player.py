class Player():

    def __init__(self, name: str, age: int, height: float, weight: float):
        self.__name = name
        self.__age = age
        self.__height = height
        self.__weight = weight


    @property
    def name(self):
        return self.__name


    @property
    def age(self):
        return self.__age


    @property
    def height(self):
        return self.__height


    @property
    def weight(self):
        return self.__weight