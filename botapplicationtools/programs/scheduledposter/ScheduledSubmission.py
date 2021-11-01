from datetime import datetime


class ScheduledSubmission:
    """Class representing a scheduled submission"""

    __url: str
    __subreddit: str
    __title: str
    __scheduledTime: datetime
    __flairId: str

    def __init__(
            self,
            url: str,
            subreddit: str,
            title: str,
            scheduledTime: datetime,
            flairId: str = None,
    ):

        self.__url = url
        self.__subreddit = subreddit
        self.__title = title
        self.__scheduledTime = scheduledTime
        self.__flairId = flairId

    @property
    def getUrl(self):
        return self.__url

    @property
    def getSubreddit(self):
        return self.__subreddit

    @property
    def getTitle(self):
        return self.__title

    @property
    def getScheduledTime(self):
        return self.__scheduledTime

    @property
    def getFlairId(self):
        return self.__flairId
