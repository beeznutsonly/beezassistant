from configparser import ConfigParser

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.programtools.featuretestertools.FeatureTesterDAO import FeatureTesterDAO
from botapplicationtools.programs.surveyresponseprocessor import SurveyResponseProcessor
from botapplicationtools.programs.surveyresponseprocessor.RedditTools import RedditTools
from botapplicationtools.programs.surveyresponseprocessor.UserMessage import UserMessage
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory


class SurveyResponseProcessorRunner(ProgramRunner):

    __redditInterfaceFactory: RedditInterfaceFactory
    __databaseConnectionFactory: DatabaseConnectionFactory
    __userProfile: str

    __subredditName: str
    __userMessage: UserMessage
    __userFlairId: str
    __testingWindow: int

    def __init__(
            self,
            redditInterfaceFactory: RedditInterfaceFactory,
            databaseConnectionFactory: DatabaseConnectionFactory,
            configReader: ConfigParser
    ):
        super().__init__()
        self.__redditInterfaceFactory = redditInterfaceFactory
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__initializeSurveyResponseProcessorRunner(configReader)

    def __initializeSurveyResponseProcessorRunner(self, configReader: ConfigParser):

        section = "SurveyResponseProcessorRunner"
        userProfile = configReader.get(
            section, "userProfile"
        )
        subredditName = configReader.get(
            section, "subredditName"
        )
        messageSubject = configReader.get(
            section, "messageSubject"
        )
        messageBody = bytes(
            configReader.get(
                section, "messageBody"
            ), "utf-8"
        ).decode("unicode_escape")
        userFlairId = configReader.get(
            section, "userFlairId"
        )
        testingWindow = configReader.getint(
            section, "testingWindow"
        )

        self.__userProfile = userProfile

        self.__subredditName = subredditName
        self.__userMessage = UserMessage(
            messageSubject,
            messageBody
        )
        self.__userFlairId = userFlairId
        self.__testingWindow = testingWindow

    def run(self):

        # First confirm that the program runner is not shutdown
        if self._informIfShutDown():
            return

        programRunnerLogger = \
            self._programRunnerLogger

        with self.__databaseConnectionFactory.getConnection() \
                as databaseConnection:

            # Executing the program
            programRunnerLogger.info(
                'Survey Response Processor is now running'
            )

            redditTools = RedditTools(
                self.__redditInterfaceFactory.getRedditInterface(
                    self.__userProfile
                ).getPrawReddit,
                self.__subredditName,
                self.__userFlairId
            )

            SurveyResponseProcessor.execute(
                redditTools,
                FeatureTesterDAO(
                    databaseConnection
                ),
                self.__userMessage,
                self.__testingWindow
            )

        # Disposing of the database connection
        self.__databaseConnectionFactory.yieldConnection(
            databaseConnection
        )

        programRunnerLogger.info(
            'Survey Response Processor completed'
        )
