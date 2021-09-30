from botapplicationtools.programs.scheduledcrossposter.CompletedCrosspostDAO import CompletedCrosspostDAO
from botapplicationtools.programs.scheduledcrossposter.ScheduledCrosspostDAO import ScheduledCrosspostDAO


class ScheduledCrossposterStorage:

    __scheduledCrosspostDAO: ScheduledCrosspostDAO
    __completedCrosspostDAO: CompletedCrosspostDAO

    def __init__(
            self,
            scheduledCrosspostDAO: ScheduledCrosspostDAO,
            completedCrosspostDAO: CompletedCrosspostDAO
    ):
        self.__scheduledCrosspostDAO = scheduledCrosspostDAO
        self.__completedCrosspostDAO = completedCrosspostDAO

    @property
    def getScheduledCrosspostDAO(self):
        return self.__scheduledCrosspostDAO

    @property
    def getCompletedCrosspostDAO(self):
        return self.__completedCrosspostDAO
