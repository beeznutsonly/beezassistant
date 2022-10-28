from configparser import ConfigParser

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.scheduledposter.ScheduledPoster import ScheduledPoster
from botapplicationtools.programs.scheduledposter.CompletedSubmissionDAO import CompletedSubmissionDAO
from botapplicationtools.programs.scheduledposter.ScheduledPosterStorage import ScheduledPosterStorage
from botapplicationtools.programs.scheduledposter.ScheduledSubmissionDAO import ScheduledSubmissionDAO
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory


class ScheduledPosterRunner(ProgramRunner):
    """
    Class responsible for running multiple
    Scheduled Poster program instances
    """

    def __init__(
            self,
            redditInterfaceFactory: RedditInterfaceFactory,
            databaseConnectionFactory: DatabaseConnectionFactory,
            configReader: ConfigParser
    ):
        super().__init__(
            redditInterfaceFactory,
            databaseConnectionFactory,
            "Scheduled Poster Runner"
        )
        self.__initializeProgramRunner(configReader)

    def __initializeProgramRunner(self, configReader: ConfigParser):
        """Initializing the Scheduled Poster Runner"""

        # Retrieving program runner variables from the config. file

        section = "ScheduledPosterRunner"
        userProfile = configReader.get(
            section, "userProfile"
        )

        self._userProfile = userProfile

    def _runCore(self, redditInterface, connection):

        prawReddit = redditInterface.getPrawReddit

        scheduledPosterStorage = ScheduledPosterStorage(
            ScheduledSubmissionDAO(connection),
            CompletedSubmissionDAO(connection)
        )

        scheduledPoster = ScheduledPoster(
            prawReddit,
            scheduledPosterStorage,
            self.isShutDown
        )

        scheduledPoster.execute()
