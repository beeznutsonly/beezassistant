# -*- coding: utf-8 -*
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmission \
    import SceneInfoSubmission


class StarSceneInfoSubmissionDetail:
    """
    Class holding Scene Info Submission details
    for a particular star
    """

    __starName: str
    __sceneInfoSubmission: SceneInfoSubmission

    def __init__(
            self,
            starName: str,
            sceneInfoSubmission: SceneInfoSubmission
    ):
        self.__starName = starName
        self.__sceneInfoSubmission = sceneInfoSubmission

    @property
    def getStarName(self):
        return self.__starName

    @property
    def getSceneInfoSubmission(self):
        return self.__sceneInfoSubmission
