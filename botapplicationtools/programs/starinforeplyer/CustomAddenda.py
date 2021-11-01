class CustomAddenda:
    """
    Class holding additional information
    specified by the user to be added to
    a star info reply
    """

    __submissionSummaryAddendum: str
    __footer: str

    def __init__(
            self,
            submissionSummaryAddendum,
            footer
    ):
        self.__submissionSummaryAddendum = submissionSummaryAddendum
        self.__footer = footer

    @property
    def getSubmissionSummaryAddendum(self):
        """
        Text to be added after the submission
        summary section of the star info reply
        """
        return self.__submissionSummaryAddendum

    @property
    def getFooter(self):
        """
        The star info reply footer
        """
        return self.__footer
