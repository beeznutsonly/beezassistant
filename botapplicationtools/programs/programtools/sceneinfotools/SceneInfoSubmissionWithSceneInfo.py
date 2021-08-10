#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Class holding both submission-specific and
scene-specific information for the submission
"""


class SceneInfoSubmissionWithSceneInfo:

    __sceneInfoSubmission = None
    __sceneInfo = None

    def __init__(self, sceneInfoSubmission, sceneInfo):
        self.__sceneInfoSubmission = sceneInfoSubmission
        self.__sceneInfo = sceneInfo

    def getSceneInfoSubmission(self):
        return self.__sceneInfoSubmission

    def getSceneInfo(self):
        return self.__sceneInfo
