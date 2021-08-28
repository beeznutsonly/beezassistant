from psaw import PushshiftAPI

from botapplicationtools.programs.sceneinfostoragearchiver.SceneInfoSubmissionsWithSceneInfoStorage import \
    SceneInfoSubmissionsWithSceneInfoStorage
from botapplicationtools.programs.sceneinfostoragearchiver.SubredditSearchParameters import SubredditSearchParameters


class SceneInfoStorageArchiverTools:

    __pushShiftAPI: PushshiftAPI
    __subredditSearchParameters: SubredditSearchParameters
    __sceneInfoSubmissionsWithSceneInfoStorage: \
        SceneInfoSubmissionsWithSceneInfoStorage

    def __init__(
            self,
            pushShiftAPI,
            subredditSearchParameters,
            sceneInfoSubmissionsWithSceneInfoStorage
    ):

        self.__pushShiftAPI = pushShiftAPI
        self.__subredditSearchParameters = subredditSearchParameters
        self.__sceneInfoSubmissionsWithSceneInfoStorage = \
            sceneInfoSubmissionsWithSceneInfoStorage

    def getPushShiftAPI(self):
        return self.__pushShiftAPI

    def getSubredditSearchParameters(self):
        return self.__subredditSearchParameters

    def getSceneInfoSubmissionsWithSceneInfoStorage(self):
        return self.__sceneInfoSubmissionsWithSceneInfoStorage
