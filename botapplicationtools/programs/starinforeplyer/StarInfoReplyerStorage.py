# -*- coding: utf-8 -*
from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetailDAO \
    import StarSceneInfoSubmissionDetailDAO
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerCommentedDAO \
    import StarInfoReplyerCommentedDAO
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerExcludedDAO \
    import StarInfoReplyerExcludedDAO
from botapplicationtools.programs.starinforeplyer.StarStorage import StarStorage


class StarInfoReplyerStorage:
    """
    Class holding storage tools used by the
    Star Info Replyer
    """

    __starInfoReplyerCommentedDAO: StarInfoReplyerCommentedDAO
    __starInfoReplyerExcludedDAO: StarInfoReplyerExcludedDAO
    __starSceneInfoSubmissionDetailDAO: StarSceneInfoSubmissionDetailDAO
    __starStorage: StarStorage

    def __init__(
            self,
            starInfoReplyerCommentedDAO,
            starInfoReplyerExcludedDAO,
            starSceneInfoSubmissionDetailDAO,
            starStorage
    ):
        self.__starInfoReplyerCommentedDAO = \
            starInfoReplyerCommentedDAO
        self.__starInfoReplyerExcludedDAO = \
            starInfoReplyerExcludedDAO
        self.__starSceneInfoSubmissionDetailDAO = \
            starSceneInfoSubmissionDetailDAO
        self.__starStorage = starStorage

    @property
    def getStarInfoReplyerCommentedDAO(self):
        return self.__starInfoReplyerCommentedDAO

    @property
    def getStarInfoReplyerExcludedDAO(self):
        return self.__starInfoReplyerExcludedDAO

    @property
    def getStarSceneInfoSubmissionDetailDAO(self):
        return self.__starSceneInfoSubmissionDetailDAO

    @property
    def getStarStorage(self):
        return self.__starStorage
