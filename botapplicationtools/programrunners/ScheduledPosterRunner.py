from configparser import ConfigParser

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.scheduledposter import ScheduledPoster
from botapplicationtools.programs.scheduledposter.CompletedSubmissionDAO import CompletedSubmissionDAO
from botapplicationtools.programs.scheduledposter.ScheduledPosterStorage import ScheduledPosterStorage
from botapplicationtools.programs.scheduledposter.ScheduledSubmissionAutoReplyDAO import ScheduledSubmissionAutoReplyDAO
from botapplicationtools.programs.scheduledposter.ScheduledSubmissionDAO import ScheduledSubmissionDAO
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory


class ScheduledPosterRunner(ProgramRunner):

    __redditInterfaceFactory: RedditInterfaceFactory
    __databaseConnectionFactory: DatabaseConnectionFactory
    __userProfile: str

    def __init__(
            self,
            databaseConnectionFactory: DatabaseConnectionFactory,
            redditInterfaceFactory: RedditInterfaceFactory,
            configReader: ConfigParser
    ):
        super().__init__()
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__redditInterfaceFactory = redditInterfaceFactory
        self.__initializeRunner(configReader)

    def __initializeRunner(self, configReader: ConfigParser):

        # Retrieving values from Config. Reader
        self._programRunnerLogger.debug(
            "Retrieving Scheduled Poster Runner initial "
            "values from the config. reader"
        )

        section = "ScheduledPosterRunner"
        userProfile = configReader.get(
            section, "userProfile"
        )

        # Initialization of instance variables

        self.__userProfile = userProfile

    def run(self):

        # Quick shutdown check before proceeding
        if self._informIfShutDown():
            return

        programRunnerLogger = self._programRunnerLogger

        # Running the program
        try:

            programRunnerLogger.info('Scheduled Poster is now running')

            with self.__databaseConnectionFactory.getConnection() \
                    as connection:

                prawReddit = self.__redditInterfaceFactory \
                    .getRedditInterface(
                        self.__userProfile
                    ).getPrawReddit

                scheduledPosterStorage = ScheduledPosterStorage(
                    ScheduledSubmissionDAO(connection),
                    CompletedSubmissionDAO(connection),
                    ScheduledSubmissionAutoReplyDAO(connection)
                )

                ScheduledPoster.execute(
                    prawReddit,
                    scheduledPosterStorage,
                    self.isShutDown
                )

                if self.isShutDown():
                    programRunnerLogger.info(
                        "Scheduled Poster successfully shut down"
                    )
                else:
                    programRunnerLogger.info(
                        "Scheduled Poster Completed"
                    )

        # Handle in the event of a program crash
        except Exception as ex:
            programRunnerLogger.error(
                "A terminal error occurred while running the Scheduled "
                "Poster: " + str(ex.args), exc_info=True
            )
        finally:

            # Dispose of database connection
            self.__databaseConnectionFactory.yieldConnection(
                connection
            )
