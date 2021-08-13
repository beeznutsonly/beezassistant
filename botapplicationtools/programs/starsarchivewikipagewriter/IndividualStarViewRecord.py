# -*- coding: utf-8 -*

"""
Class holding a single Star view record/item
"""


class IndividualStarViewRecord:

    __submissionId = None
    __star = None
    __title = None

    def __init__(self, submissionId, star, title):
        self.__submissionId = submissionId
        self.__star = star
        self.__title = title
    
    def getSubmissionId(self):
        return self.__submissionId

    def getStar(self):
        return self.__star

    def getTitle(self):
        return self.__title