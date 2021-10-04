from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.scheduledcrossposter import ScheduledCrossposter
from botapplicationtools.programs.scheduledcrossposter.CompletedCrosspostDAO import CompletedCrosspostDAO
from botapplicationtools.programs.scheduledcrossposter.ScheduledCrosspostDAO import ScheduledCrosspostDAO
from botapplicationtools.programs.scheduledcrossposter.ScheduledCrossposterStorage import ScheduledCrossposterStorage
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory


class ScheduledCrossposterRunner(ProgramRunner):

    __redditInterfaceFactory: RedditInterfaceFactory
    __databaseConnectionFactory: DatabaseConnectionFactory
    __userProfile: str

    __subreddit: str

    def __init__(
            self,
            databaseConnectionFactory: DatabaseConnectionFactory,
            redditInterfaceFactory: RedditInterfaceFactory,
            configReader: ConfigParser
    ):
        super().__init__()
        self.__redditInterfaceFactory = redditInterfaceFactory
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__initializeRunner(configReader)

    def __initializeRunner(self, configReader: ConfigParser):

        # Retrieving values from Config. Reader
        self._programRunnerLogger.debug(
            "Retrieving Scheduled Crossposter Runner initial "
            "values from the config. reader"
        )

        section = "ScheduledCrossposterRunner"
        subreddit = configReader.get(
            section, "subreddit"
        )
        userProfile = configReader.get(
            section, "userProfile"
        )

        # Initialization of instance variables

        self.__subreddit = subreddit
        self.__userProfile = userProfile

    def run(self):

        # Quick shutdown check before proceeding
        if self._informIfShutDown():
            return

        programRunnerLogger = self._programRunnerLogger

        # Running the program
        try:

            programRunnerLogger.info('Scheduled Crossposter is now running')

            with self.__databaseConnectionFactory.getConnection() \
                    as connection:

                prawReddit = self.__redditInterfaceFactory \
                    .getRedditInterface(
                        self.__userProfile
                    ).getPrawReddit

                submissionStream = prawReddit.subreddit(
                    self.__subreddit
                ).stream.submissions(pause_after=0)

                scheduledCrossposterStorage = ScheduledCrossposterStorage(
                    ScheduledCrosspostDAO(connection),
                    CompletedCrosspostDAO(connection)
                )

                ScheduledCrossposter.execute(
                    submissionStream,
                    scheduledCrossposterStorage,
                    ThreadPoolExecutor(),
                    self.isShutDown
                )

                if self.isShutDown():
                    programRunnerLogger.info(
                        "Scheduled Crossposter successfully shut down"
                    )
                else:
                    programRunnerLogger.info(
                        "Scheduled Crossposter Completed"
                    )

        # Handle in the event of a program crash
        except Exception as ex:
            programRunnerLogger.error(
                "A terminal error occurred while running the Scheduled "
                "Crossposter: " + str(ex.args), exc_info=True
            )
        finally:

            # Dispose of database connection
            self.__databaseConnectionFactory.yieldConnection(
                connection
            )
