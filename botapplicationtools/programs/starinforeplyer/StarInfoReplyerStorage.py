# -*- coding: utf-8 -*
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerCommentedDAO \
    import StarInfoReplyerCommentedDAO
from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetailDAO \
    import StarSceneInfoSubmissionDetailDAO


class StarInfoReplyerStorage:
    """
    Class holding storage tools used by the
    Star Info Replyer
    """

    __starInfoReplyerCommentedDAO: StarInfoReplyerCommentedDAO
    __starSceneInfoSubmissionDetailDAO: StarSceneInfoSubmissionDetailDAO

    def __init__(
            self,
            starInfoReplyerCommentedDAO,
            starSceneInfoSubmissionDetailDAO
    ):
        self.__starInfoReplyerCommentedDAO = \
            starInfoReplyerCommentedDAO
        self.__starSceneInfoSubmissionDetailDAO = \
            starSceneInfoSubmissionDetailDAO

    @property
    def getStarInfoReplyerCommentedDAO(self):
        return self.__starInfoReplyerCommentedDAO

    @property
    def getStarSceneInfoSubmissionDetailDAO(self):
        return self.__starSceneInfoSubmissionDetailDAO
