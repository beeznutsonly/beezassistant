# -*- coding: utf-8 -*
from praw import Reddit
from psaw import PushshiftAPI


class RedditInterface:
    """
    Class holding tools to interface with the Reddit API
    """

    __prawReddit: Reddit
    __pushShiftAPI: PushshiftAPI

    def __init__(self, prawReddit):
        self.__prawReddit = prawReddit
        self.__pushShiftAPI = PushshiftAPI(prawReddit)

    @property
    def getPrawReddit(self):
        """Retrieve the interface's PrawReddit instance"""

        return self.__prawReddit

    @property
    def getPushShiftAPI(self):
        """Retrieve the interface's PushshiftAPI instance"""

        return self.__pushShiftAPI
