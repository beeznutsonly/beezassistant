import re
from configparser import ConfigParser

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.programtools.starnotificationtools.StarNotificationSubscriptionDAO import \
    StarNotificationSubscriptionDAO
from botapplicationtools.programs.starnotifier.StarNotifier import StarNotifier
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
        super().__init__(
            redditInterfaceFactory,
            databaseConnectionFactory,
            "Star Notifier Runner"
        )
        self.__redditInterfaceFactory = redditInterfaceFactory
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__initializeStarNotifierRunner(configReader)

    def __initializeStarNotifierRunner(
            self,
            configReader: ConfigParser
    ):
        """Initialize the Star Notifier Runner"""

        # Retrieving values from configuration file

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

        self._userProfile = userProfile
        self.__sceneInfoTools = SceneInfoTools(
            re.compile(r'{}'.format(sceneInfoCommentMatcher)),
            re.compile(r'{}'.format(starMatcher)),
            re.compile(r'{}'.format(sceneInfoFlairId))
        )
        self.__subreddit = subreddit

    def _runCore(self, redditInterface, connection):

        # Setting up the Notifier's Reddit Tools
        prawReddit = redditInterface.getPrawReddit
        redditTools = RedditTools(
            prawReddit,
            self.__subreddit
        )

        # Storage tools for the Star Notifier
        starNotificationSubscriptionDAO = StarNotificationSubscriptionDAO(
            connection
        )

        # Executing the program
        starNotifier = StarNotifier(
            redditTools,
            starNotificationSubscriptionDAO,
            self.__sceneInfoTools,
            self.isShutDown
        )
        starNotifier.execute()
