# -*- coding: utf-8 -*

"""
Class holding tools to interface with the Reddit API
"""

from psaw import PushshiftAPI


class RedditInterface:

    __prawReddit = None
    __pushShiftAPI = None

    def __init__(self, prawReddit):
        self.__prawReddit = prawReddit
        self.__pushShiftAPI = PushshiftAPI(prawReddit)

    def getPrawReddit(self):
        return self.__prawReddit

    def getPushShiftAPI(self):
        return self.__pushShiftAPI
