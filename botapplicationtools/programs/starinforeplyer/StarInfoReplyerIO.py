from botapplicationtools.programs.starinforeplyer.RedditTools import RedditTools
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerStorage import StarInfoReplyerStorage


class StarInfoReplyerIO:
    """Class holding IO tools used by the Star Info Replyer"""

    __starInfoReplyerStorage: StarInfoReplyerStorage
    __redditTools: RedditTools

    def __init__(
            self,
            starInfoReplyerStorage: StarInfoReplyerStorage,
            redditTools: RedditTools
    ):

        self.__starInfoReplyerStorage = starInfoReplyerStorage
        self.__redditTools = redditTools

    @property
    def getStarInfoReplyerStorage(self):
        return self.__starInfoReplyerStorage

    @property
    def getRedditTools(self):
        return self.__redditTools
