from praw import Reddit
from praw.models import Subreddit


class RedditTools:

    __prawReddit: Reddit
    __subreddit: Subreddit
    __userFlairId: str

    def __init__(
            self,
            prawReddit: Reddit,
            subredditName: str,
            userFlairId
    ):
        self.__prawReddit = prawReddit
        self.__subreddit = prawReddit.subreddit(
            subredditName
        )
        self.__userFlairId = userFlairId

    @property
    def getPrawReddit(self):
        return self.__prawReddit

    @property
    def getSubreddit(self):
        return self.__subreddit

    @property
    def getUserFlairId(self):
        return self.__userFlairId
