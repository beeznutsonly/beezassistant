class CustomAddenda:

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
        return self.__submissionSummaryAddendum

    @property
    def getFooter(self):
        return self.__footer
