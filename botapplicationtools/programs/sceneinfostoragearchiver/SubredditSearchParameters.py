# -*- coding: utf-8 -*
from botapplicationtools.programs.sceneinfostoragearchiver.Extractors import Extractors


class SubredditSearchParameters:
    """
    Class holding subreddit-specific details
    on retrieving scene info submissions and
    the relevant scene info
    """

    __subredditName: str
    __fromTime: str
    __extractors: Extractors

    def __init__(self, subredditName, fromTime, extractors):
        self.__subredditName = subredditName
        self.__fromTime = fromTime
        self.__extractors = extractors

    @property
    def getSubredditName(self):
        return self.__subredditName

    @property
    def getFromTime(self):
        return self.__fromTime

    @property
    def getExtractors(self):
        return self.__extractors
