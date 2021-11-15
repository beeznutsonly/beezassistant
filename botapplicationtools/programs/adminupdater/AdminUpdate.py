class AdminUpdate:

    def __init__(
            self,
            ID: int,
            heading: str,
            details: str
    ):
        self.__id = ID
        self.__heading = heading
        self.__details = details

    @property
    def getId(self):
        return self.__id

    @property
    def getHeading(self):
        return self.__heading

    @property
    def getDetails(self):
        return self.__details
