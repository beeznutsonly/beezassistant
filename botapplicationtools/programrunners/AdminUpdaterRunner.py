from configparser import ConfigParser

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.adminupdater.AdminUpdateDAO import AdminUpdateDAO
from botapplicationtools.programs.adminupdater.AdminUpdater import AdminUpdater
from botapplicationtools.programs.adminupdater.FormattingTools import FormattingTools
from botapplicationtools.programs.adminupdater.RedditTools import RedditTools
from botapplicationtools.programs.programtools.generaltools.RedditInterface import RedditInterface
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory


class AdminUpdaterRunner(ProgramRunner):
    """
    Class responsible for running multiple
    Admin Updater instances
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
            "Admin Updater Runner"
        )
        self.__initializeProgramRunner(configReader)

    def __initializeProgramRunner(self, configReader: ConfigParser):

        # Retrieving values from config. file
        section = "AdminUpdaterRunner"
        userProfile = configReader.get(
            section, "userProfile"
        )
        subredditName = configReader.get(
            section, "subredditName"
        )
        wikiPageName = configReader.get(
            section, "wikiPageName"
        )
        widgetID = configReader.get(
            section, "widgetID"
        )
        wikiUpdateFormat = configReader.get(
            section, "wikiUpdateFormat"
        )
        widgetUpdateFormat = configReader.get(
            section, "widgetUpdateFormat"
        )
        dateFormat = configReader.get(
            section, "dateFormat"
        )
        maxWidgetLines = configReader.getint(
            section, "maxWidgetLines"
        )
        widgetFooter = configReader.get(
            section, "widgetFooter"
        )

        # Instance variable processing and assignment
        self._userProfile = userProfile
        self.__subredditName = subredditName
        self.__wikiPageName = wikiPageName
        self.__widgetID = widgetID
        self.__formattingTools = FormattingTools(
            bytes(
                wikiUpdateFormat,
                "utf-8"
            ).decode("unicode_escape"),
            bytes(
                widgetUpdateFormat,
                "utf-8"
            ).decode("unicode_escape"),
            dateFormat,
            maxWidgetLines,
            bytes(
                widgetFooter,
                "utf-8"
            ).decode("unicode_escape"),
        )

    def _runCore(self, redditInterface: RedditInterface, connection):

        # Setting up program parameters
        subreddit = redditInterface.getPrawReddit.subreddit(
            self.__subredditName
        )
        redditTools = RedditTools(
            subreddit,
            self.__wikiPageName,
            self.__widgetID
        )

        # Executing the program
        adminUpdater = AdminUpdater(
            AdminUpdateDAO(connection),
            redditTools,
            self.__formattingTools,
            self.isShutDown
        )
        adminUpdater.execute()
