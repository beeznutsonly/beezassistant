import re
from configparser import ConfigParser

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.programtools.starnotificationtools.StarNotificationSubscriptionDAO import \
    StarNotificationSubscriptionDAO
from botapplicationtools.programs.starnotifier import StarNotifier
from botapplicationtools.programs.starnotifier.RedditTools import RedditTools
from botapplicationtools.programs.starnotifier.SceneInfoTools import SceneInfoTools
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory


class StarNotifierRunner(ProgramRunner):
    """
    Class responsible for running multiple
    StarNotifier program instances
    """

    __redditInterfaceFactory: RedditInterfaceFactory
    __databaseConnectionFactory: DatabaseConnectionFactory
    __userProfile: str

    __sceneInfoTools: SceneInfoTools
    __subreddit: str

    def __init__(
            self,
            redditInterfaceFactory: RedditInterfaceFactory,
            databaseConnectionFactory: DatabaseConnectionFactory,
            configReader: ConfigParser
    ):
        super().__init__()
        self.__redditInterfaceFactory = redditInterfaceFactory
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__initializeStarNotifierRunner(configReader)

    def __initializeStarNotifierRunner(
            self,
            configReader: ConfigParser
    ):
        """Initialize the Star Notifier Runner"""

        # Retrieving values from configuration file

        self._programRunnerLogger.debug(
            "Retrieving Star Notifier Runner initial "
            "values from the config. reader"
        )
        section = "StarNotifierRunner"
        userProfile = configReader.get(
            section, "userProfile"
        )
        sceneInfoCommentMatcher = configReader.get(
            section, "sceneInfoCommentMatcher"
        )
        starMatcher = configReader.get(
            section, "starMatcher"
        )
        sceneInfoFlairId = configReader.get(
            section, "sceneInfoFlairId"
        )
        subreddit = configReader.get(
            section, "subreddit"
        )

        self.__userProfile = userProfile
        self.__sceneInfoTools = SceneInfoTools(
            re.compile(r'{}'.format(sceneInfoCommentMatcher)),
            re.compile(r'{}'.format(starMatcher)),
            re.compile(r'{}'.format(sceneInfoFlairId))
        )
        self.__subreddit = subreddit

    def run(self):

        # First confirm that the program runner is not shutdown
        if self._informIfShutDown():
            return

        programRunnerLogger = self._programRunnerLogger

        try:

            # Executing the program
            programRunnerLogger.info('Star Notifier is now running')

            # Setting up the Notifier's Reddit Tools
            prawReddit = self.__redditInterfaceFactory \
                .getRedditInterface(self.__userProfile) \
                .getPrawReddit
            redditTools = RedditTools(
                prawReddit,
                self.__subreddit
            )

            with self.__databaseConnectionFactory.getConnection() \
                    as connection:

                # Storage tools for the Star Notifier
                starNotificationSubscriptionDAO = StarNotificationSubscriptionDAO(
                    connection
                )

                # Executing the program
                StarNotifier.execute(
                    redditTools,
                    starNotificationSubscriptionDAO,
                    self.__sceneInfoTools,
                    self.isShutDown
                )

            # Program termination message determination
            if self.isShutDown():
                programRunnerLogger.info(
                    'Star Notifier successfully shut down'
                )
            else:
                programRunnerLogger.info(
                    'Star Notifier completed'
                )

        # Handle if an error occurs while running the Star Notifier
        except Exception as er:
            programRunnerLogger.error(
                "A terminal error occurred while running the Star "
                "Notifier: " + str(er.args), exc_info=True
            )
        finally:
            # Dispose of database connection
            self.__databaseConnectionFactory.yieldConnection(
                connection
            )
