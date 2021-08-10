# -*- coding: utf-8 -*

"""
Class holding "Extractors" i.e. tools to filter out
both scene info submissions and the relevant scene info
"""


class Extractors:

    __sceneInfoFlairID = None
    __sceneInfoTextMatcher = None
    __movieNameExtractor = None
    __starNamesExtractor = None

    def __init__(
            self,
            sceneInfoFlairID,
            sceneInfoTextMatcher,
            movieNameExtractor,
            starNamesExtractor
    ):
        self.__sceneInfoFlairID = sceneInfoFlairID
        self.__sceneInfoTextMatcher = sceneInfoTextMatcher
        self.__movieNameExtractor = movieNameExtractor
        self.__starNamesExtractor = starNamesExtractor

    def getSceneInfoFlairID(self):
        return self.__sceneInfoFlairID

    def getSceneInfoTextMatcher(self):
        return self.__sceneInfoTextMatcher

    def getMovieNameExtractor(self):
        return self.__movieNameExtractor

    def getStarNamesExtractor(self):
        return self.__starNamesExtractor