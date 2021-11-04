from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.scheduledcrossposter.ScheduledCrossposter import ScheduledCrossposter
from botapplicationtools.programs.scheduledcrossposter.CompletedCrosspostDAO import CompletedCrosspostDAO
from botapplicationtools.programs.scheduledcrossposter.ScheduledCrosspostDAO import ScheduledCrosspostDAO
from botapplicationtools.programs.scheduledcrossposter.ScheduledCrossposterStorage import ScheduledCrossposterStorage
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory


class ScheduledCrossposterRunner(ProgramRunner):
    """
    Class responsible for running multiple
    Scheduled Crossposter program instances
    """

    __subreddit: str

    def __init__(
            self,
            redditInterfaceFactory: RedditInterfaceFactory,
            databaseConnectionFactory: DatabaseConnectionFactory,
            configReader: ConfigParser
    ):
        super().__init__(
            redditInterfaceFactory,
            databaseConnectionFactory,
            "Scheduled Crossposter Runner"
        )
        self.__initializeProgramRunner(configReader)

    def __initializeProgramRunner(self, configReader: ConfigParser):
        """Initialize the Scheduled Crossposter Runner"""

        section = "ScheduledCrossposterRunner"
        userProfile = configReader.get(
            section, "userProfile"
        )
        subreddit = configReader.get(
            section, "subreddit"
        )

        # Initialization of instance variables

        self._userProfile = userProfile
        self.__subreddit = subreddit

    def _runCore(self, redditInterface, connection):

        prawReddit = redditInterface.getPrawReddit

        submissionStream = prawReddit.subreddit(
            self.__subreddit
        ).stream.submissions(pause_after=0)

        scheduledCrossposterStorage = ScheduledCrossposterStorage(
            ScheduledCrosspostDAO(connection),
            CompletedCrosspostDAO(connection)
        )

        scheduledCrossposter = ScheduledCrossposter(
            submissionStream,
            scheduledCrossposterStorage,
            ThreadPoolExecutor,
            self.isShutDown
        )

        scheduledCrossposter.execute()
