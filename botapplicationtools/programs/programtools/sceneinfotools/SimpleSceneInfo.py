# -*- coding: utf-8 -*

from typing import List


class SimpleSceneInfo:
    """
    Class holding a submission's scene info
    """

    __movieName: str
    __stars: List[str]

    def __init__(self, movieName, *stars):
        self.__movieName = movieName
        self.__stars = list(stars)

    @property
    def getMovieName(self):
        """Retrieve the movie name"""

        return str(self.__movieName)

    @property
    def getStars(self):
        """Retrieve the list of stars from the scene"""

        return list(self.__stars)
