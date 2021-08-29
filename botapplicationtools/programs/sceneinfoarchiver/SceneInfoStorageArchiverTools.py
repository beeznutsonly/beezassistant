# -*- coding: utf-8 -*

from psaw import PushshiftAPI

from botapplicationtools.programs.sceneinfostoragearchiver \
    .SceneInfoSubmissionsWithSceneInfoStorage import \
    SceneInfoSubmissionsWithSceneInfoStorage
from botapplicationtools.programs.sceneinfostoragearchiver \
    .SubredditSearchParameters import SubredditSearchParameters


class SceneInfoStorageArchiverTools:
    """
    Class holding tools required by the scene info storage
    archiver program
    """

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

    @property
    def getPushShiftAPI(self):
        return self.__pushShiftAPI

    @property
    def getSubredditSearchParameters(self):
        return self.__subredditSearchParameters

    @property
    def getSceneInfoSubmissionsWithSceneInfoStorage(self):
        return self.__sceneInfoSubmissionsWithSceneInfoStorage
