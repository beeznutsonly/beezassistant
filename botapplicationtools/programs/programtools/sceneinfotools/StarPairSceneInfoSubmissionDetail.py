# -*- coding: utf-8 -*
from typing import Tuple

from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmission \
    import SceneInfoSubmission


class StarPairSceneInfoSubmissionDetail:
    """
    Class holding Scene Info Submission details
    for a particular star pair
    """

    def __init__(
            self,
            starNames: Tuple[str, str],
            sceneInfoSubmission: SceneInfoSubmission
    ):
        self.__starNames = starNames
        self.__sceneInfoSubmission = sceneInfoSubmission

    @property
    def getStarNames(self):
        return self.__starNames

    @property
    def getSceneInfoSubmission(self):
        return self.__sceneInfoSubmission
