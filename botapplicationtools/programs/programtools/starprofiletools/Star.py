from datetime import date


class Star:
    """Class encapsulating a Star's Profile"""

    __name: str
    __birthday: date
    __nationality: str
    __birthPlace: str
    __yearsActive: str
    __description: str

    def __init__(
            self,
            name: str,
            birthday: date,
            nationality: str,
            birthPlace: str,
            yearsActive: str,
            description: str
    ):
        self.__name = name
        self.__birthday = birthday
        self.__nationality = nationality
        self.__birthPlace = birthPlace
        self.__yearsActive = yearsActive
        self.__description = description

    @property
    def getName(self):
        return self.__name

    @property
    def getBirthday(self):
        return self.__birthday

    @property
    def getNationality(self):
        return self.__nationality

    @property
    def getBirthPlace(self):
        return self.__birthPlace

    @property
    def getYearsActive(self):
        return self.__yearsActive

    @property
    def getDescription(self):
        return self.__description
