class StarNotificationSubscription:

    __username: str
    __star: str

    def __init__(
            self,
            username: str,
            star: str
    ):
        self.__username = username
        self.__star = star

    @property
    def getUsername(self):
        return self.__username

    @property
    def getStar(self):
        return self.__star
