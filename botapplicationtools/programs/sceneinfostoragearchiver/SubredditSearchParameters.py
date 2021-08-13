# -*- coding: utf-8 -*

"""
Class holding subreddit-specific details
on retrieving scene info submissions and
the relevant scene info
"""


class SubredditSearchParameters:

    __subredditName = None
    __fromTime = None
    __extractors = None

    def __init__(self, subredditName, fromTime, extractors):
        self.__subredditName = subredditName
        self.__fromTime = fromTime
        self.__extractors = extractors

    def getSubredditName(self):
        return self.__subredditName

    def getFromTime(self):
        return self.__fromTime

    def getExtractors(self):
        return self.__extractors