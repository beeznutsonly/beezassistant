# -*- coding: utf-8 -*

"""
Class holding a submission's scene info
"""


class SceneInfo:
    
    __movieName = None
    __stars = None

    def __init__(self, movieName, *stars):
        self.__movieName = movieName
        self.__stars = list(stars)

    def getMovieName(self):
        return str(self.__movieName)

    def getStars(self):
        return list(self.__stars)