from datetime import datetime


class ScheduledCrosspost:
    """Class representing a scheduled crosspost"""

    __url: str
    __subreddit: str
    __scheduledTime: datetime
    __title: str

    def __init__(
            self,
            url: str,
            subreddit: str,
            scheduledTime: datetime,
            title: str = None
    ):
        self.__url = url
        self.__subreddit = subreddit
        self.__scheduledTime = scheduledTime
        self.__title = title

    @property
    def getUrl(self):
        return self.__url

    @property
    def getSubreddit(self):
        return self.__subreddit

    @property
    def getScheduledTime(self):
        return self.__scheduledTime

    @property
    def getTitle(self):
        return self.__title
