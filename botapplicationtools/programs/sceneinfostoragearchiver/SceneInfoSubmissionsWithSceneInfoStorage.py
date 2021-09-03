# -*- coding: utf-8 -*

from botapplicationtools.programs.programtools.sceneinfotools \
    .SimpleSceneInfoDAO import SimpleSceneInfoDAO
from botapplicationtools.programs.programtools.sceneinfotools \
    .SceneInfoSubmissionDAO import SceneInfoSubmissionDAO
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmissionWithSceneInfoDAO import \
    SceneInfoSubmissionWithSceneInfoDAO


class SceneInfoSubmissionsWithSceneInfoStorage:
    """
    Class holding DAOs relevant to retrieving and
    manipulating scene info submission and scene
    info data
    """

    __sceneInfoDAO: SimpleSceneInfoDAO
    __sceneInfoSubmissionDAO: SceneInfoSubmissionDAO
    __sceneInfoSubmissionWithSceneInfoDAO: \
        SceneInfoSubmissionWithSceneInfoDAO

    def __init__(
        self,
        sceneInfoDAO, 
        sceneInfoSubmissionDAO,
        sceneInfoSubmissionWithSceneInfoDAO
    ):
        self.__sceneInfoDAO = sceneInfoDAO
        self.__sceneInfoSubmissionDAO = sceneInfoSubmissionDAO
        self.__sceneInfoSubmissionWithSceneInfoDAO = \
            sceneInfoSubmissionWithSceneInfoDAO

    @property
    def getSceneInfoDAO(self):
        """Retrieve the scene info DAO"""

        return self.__sceneInfoDAO

    @property
    def getSceneInfoSubmissionDAO(self):
        """Retrieve the scene info submission DAO"""

        return self.__sceneInfoSubmissionDAO

    @property
    def getSceneInfoSubmissionWithSceneInfoDAO(self):
        """Retrieve the scene info submission with scene info DAO"""

        return self.__sceneInfoSubmissionWithSceneInfoDAO
