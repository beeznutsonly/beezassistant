# -*- coding: utf-8 -*

class IndividualStarViewRecord:
    """
    Class representing a single IndividualStarView record/item
    """

    __submissionId: str
    __star: str
    __title: str

    def __init__(self, submissionId, star, title):
        self.__submissionId = submissionId
        self.__star = star
        self.__title = title

    @property
    def getSubmissionId(self):
        return self.__submissionId

    @property
    def getStar(self):
        return self.__star

    @property
    def getTitle(self):
        return self.__title
