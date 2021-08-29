#!/usr/bin/env python
# -*- coding: utf-8 -*-

from praw.models import Submission

from botapplicationtools.programs.programtools.sceneinfotools.SceneInfo import SceneInfo


class SceneInfoSubmissionWithSceneInfo:
    """
    Class holding both submission-specific and
    scene-specific information for the submission
    """

    __sceneInfoSubmission: Submission
    __sceneInfo: SceneInfo

    def __init__(self, sceneInfoSubmission, sceneInfo):
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
