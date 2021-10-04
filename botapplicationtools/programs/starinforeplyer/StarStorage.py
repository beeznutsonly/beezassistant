from botapplicationtools.programs.programtools.starprofiletools.StarDAO import StarDAO
from botapplicationtools.programs.programtools.starprofiletools.StarLinkDAO import StarLinkDAO


class StarStorage:

    __starDAO: StarDAO
    __starLinkDAO: StarLinkDAO

    def __init__(
            self,
            starDAO,
            starLinkDAO
    ):
        self.__starDAO = starDAO
        self.__starLinkDAO = starLinkDAO

    @property
    def getStarDAO(self):
        return self.__starDAO

    @property
    def getStarLinkDAO(self):
        return self.__starLinkDAO
