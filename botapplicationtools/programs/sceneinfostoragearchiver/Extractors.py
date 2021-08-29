# -*- coding: utf-8 -*
import re


class Extractors:
    """
    Class holding "Extractors" i.e. tools to filter out
    both scene info submissions and the relevant scene info
    """

    __sceneInfoFlairID: str
    __sceneInfoTextMatcher: re.Pattern
    __movieNameExtractor: re.Pattern
    __starNamesExtractor: re.Pattern

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

    @property
    def getSceneInfoFlairID(self):
        """Retrieve scene info flair ID"""

        return self.__sceneInfoFlairID

    @property
    def getSceneInfoTextMatcher(self):
        """Retrieve the scene info text matcher"""

        return self.__sceneInfoTextMatcher

    @property
    def getMovieNameExtractor(self):
        """Retrieve the movie name extractor"""

        return self.__movieNameExtractor

    @property
    def getStarNamesExtractor(self):
        """Retrieve the star names extractor"""

        return self.__starNamesExtractor
