# -*- coding: utf-8 -*
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerCommentedDAO \
    import StarInfoReplyerCommentedDAO
from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetailDAO \
    import StarSceneInfoSubmissionDetailDAO
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerExcludedDAO import StarInfoReplyerExcludedDAO


class StarInfoReplyerStorage:
    """
    Class holding storage tools used by the
    Star Info Replyer
    """

    __starInfoReplyerCommentedDAO: StarInfoReplyerCommentedDAO
    __starInfoReplyerExcludedDAO: StarInfoReplyerExcludedDAO
    __starSceneInfoSubmissionDetailDAO: StarSceneInfoSubmissionDetailDAO

    def __init__(
            self,
            starInfoReplyerCommentedDAO,
            starInfoReplyerExcludedDAO,
            starSceneInfoSubmissionDetailDAO
    ):
        self.__starInfoReplyerCommentedDAO = \
            starInfoReplyerCommentedDAO
        self.__starInfoReplyerExcludedDAO = \
            starInfoReplyerExcludedDAO
        self.__starSceneInfoSubmissionDetailDAO = \
            starSceneInfoSubmissionDetailDAO

    @property
    def getStarInfoReplyerCommentedDAO(self):
        return self.__starInfoReplyerCommentedDAO

    @property
    def getStarInfoReplyerExcludedDAO(self):
        return self.__starInfoReplyerExcludedDAO

    @property
    def getStarSceneInfoSubmissionDetailDAO(self):
        return self.__starSceneInfoSubmissionDetailDAO
