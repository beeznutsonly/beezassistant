# -*- coding: utf-8 -*
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerCommentedDAO import StarInfoReplyerCommentedDAO
from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarViewDAO import IndividualStarViewDAO


class StarInfoReplyerStorage:
    """
    Class holding storage tools used by the
    Star Info Replyer
    """

    __starInfoReplyerCommentedDAO: StarInfoReplyerCommentedDAO
    __individualStarViewDAO: IndividualStarViewDAO

    def __init__(
            self,
            starInfoReplyerCommentedDAO,
            individualStarViewDAO
    ):
        self.__starInfoReplyerCommentedDAO = starInfoReplyerCommentedDAO
        self.__individualStarViewDAO = individualStarViewDAO

    @property
    def getStarInfoReplyerCommentedDAO(self):
        return self.__starInfoReplyerCommentedDAO

    @property
    def getIndividualStarViewDAO(self):
        return self.__individualStarViewDAO
