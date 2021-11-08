from re import Pattern


class SceneInfoTools:
    """
    Class holding scene info tools to be used to identify
    scene info comments and extract the relevant scene info
    comments
    """

    __sceneInfoCommentMatcher: Pattern
    __starMatcher: Pattern
    __sceneInfoFlair: str

    def __init__(
            self,
            sceneInfoCommentMatcher: Pattern,
            starMatcher: Pattern,
            sceneInfoFlair: str
    ):
        self.__sceneInfoCommentMatcher = sceneInfoCommentMatcher
        self.__starMatcher = starMatcher
        self.__sceneInfoFlair = sceneInfoFlair

    @property
    def getSceneInfoCommentMatcher(self):
        return self.__sceneInfoCommentMatcher

    @property
    def getStarMatcher(self):
        return self.__starMatcher

    @property
    def getSceneInfoFlair(self):
        return self.__sceneInfoFlair
