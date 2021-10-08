from botapplicationtools.programs.programtools.starprofiletools.Star import Star


class StarLink:

    __star: Star
    __link: str
    __linkName: str

    def __init__(
            self,
            star: Star,
            link: str,
            linkName: str
    ):
        self.__star = star
        self.__link = link
        self.__linkName = linkName

    @property
    def getStar(self):
        return self.__star

    @property
    def getLink(self):
        return self.__link

    @property
    def getLinkName(self):
        return self.__linkName
