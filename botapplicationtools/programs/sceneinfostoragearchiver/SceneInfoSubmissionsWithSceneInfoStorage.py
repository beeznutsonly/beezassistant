# -*- coding: utf-8 -*

"""
Class holding DAOs relevant to retrieving and
manipulating scene info submission and scene
info data
"""


class SceneInfoSubmissionsWithSceneInfoStorage:

    __sceneInfoDAO = None
    __sceneInfoSubmissionDAO = None
    __sceneInfoSubmissionWithSceneInfoDAO = None

    def __init__(
        self,
        sceneInfoDAO, 
        sceneInfoSubmissionDAO,
        sceneInfoSubmissionWithSceneInfoDAO
    ):
        self.__sceneInfoDAO = sceneInfoDAO
        self.__sceneInfoSubmissionDAO = sceneInfoSubmissionDAO
        self.__sceneInfoSubmissionWithSceneInfoDAO = sceneInfoSubmissionWithSceneInfoDAO

    def getSceneInfoDAO(self):
        return self.__sceneInfoDAO

    def getSceneInfoSubmissionDAO(self):
        return self.__sceneInfoSubmissionDAO

    def getSceneInfoSubmissionWithSceneInfoDAO(self):
        return self.__sceneInfoSubmissionWithSceneInfoDAO
