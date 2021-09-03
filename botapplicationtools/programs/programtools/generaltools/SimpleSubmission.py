from praw.models import Submission


class SimpleSubmission:
    """
    Class encapsulating the most minimal
    representation of a submission
    """

    __submissionId: str

    def __init__(self, submissionId):
        self.__submissionId = submissionId

    @property
    def getSubmissionId(self):
        return self.__submissionId

    @classmethod
    def getSimpleSubmissionFromId(
            cls, submissionId: str
    ):
        """
        Returns a SimpleSubmission object from
        the provided submissionId
        """
        return SimpleSubmission(submissionId)

    @classmethod
    def getSimpleSubmissionFromPrawSubmission(
            cls, prawSubmission: Submission
    ):
        """
        Returns a SimpleSubmission object from
        the provided PRAW submission
        """
        return SimpleSubmission(prawSubmission.id)
