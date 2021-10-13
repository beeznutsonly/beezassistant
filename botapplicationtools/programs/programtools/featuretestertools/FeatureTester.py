from datetime import datetime


class FeatureTester:

    __username: str
    __expiry: datetime

    def __init__(
            self,
            username: str,
            expiry: datetime
    ):
        self.__username = username
        self.__expiry = expiry

    @property
    def getUsername(self):
        return self.__username

    @property
    def getExpiry(self):
        return self.__expiry
