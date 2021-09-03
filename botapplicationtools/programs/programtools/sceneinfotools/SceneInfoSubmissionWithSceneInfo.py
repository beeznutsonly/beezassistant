#!/usr/bin/env python
# -*- coding: utf-8 -*-

from botapplicationtools.programs.programtools.sceneinfotools.SimpleSceneInfo \
    import SimpleSceneInfo
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmission \
    import SceneInfoSubmission


class SceneInfoSubmissionWithSceneInfo:
    """
    Class holding both submission-specific and
    scene-specific information for the submission
    """

    __sceneInfoSubmission: SceneInfoSubmission
    __sceneInfo: SimpleSceneInfo

    def __init__(
            self,
            sceneInfoSubmission: SceneInfoSubmission,
            sceneInfo: SimpleSceneInfo
    ):
        self.__sceneInfoSubmission = sceneInfoSubmission
        self.__sceneInfo = sceneInfo

    @property
    def getSceneInfoSubmission(self):
        """Retrieve scene info submission"""

        return self.__sceneInfoSubmission

    @property
    def getSceneInfo(self):
        """Retrieve scene info"""

        return self.__sceneInfo
