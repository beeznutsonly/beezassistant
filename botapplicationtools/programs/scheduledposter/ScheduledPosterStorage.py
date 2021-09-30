from botapplicationtools.programs.scheduledposter import ScheduledSubmissionDAO, CompletedSubmissionDAO
from botapplicationtools.programs.scheduledposter.ScheduledSubmissionAutoReplyDAO import ScheduledSubmissionAutoReplyDAO


class ScheduledPosterStorage:

    __scheduledSubmissionDAO: ScheduledSubmissionDAO
    __completedSubmissionDAO: CompletedSubmissionDAO
    __scheduledSubmissionAutoReplyDAO: ScheduledSubmissionAutoReplyDAO

    def __init__(
            self,
            scheduledSubmissionDAO: ScheduledSubmissionDAO,
            completedSubmissionDAO: CompletedSubmissionDAO,
            scheduledSubmissionAutoReplyDAO: ScheduledSubmissionAutoReplyDAO
    ):

        self.__scheduledSubmissionDAO = scheduledSubmissionDAO
        self.__completedSubmissionDAO = completedSubmissionDAO
        self.__scheduledSubmissionAutoReplyDAO = scheduledSubmissionAutoReplyDAO

    @property
    def getScheduledSubmissionDAO(self):
        return self.__scheduledSubmissionDAO

    @property
    def getCompletedSubmissionDAO(self):
        return self.__completedSubmissionDAO

    @property
    def getScheduledSubmissionAutoReplyDAO(self):
        return self.__scheduledSubmissionAutoReplyDAO
