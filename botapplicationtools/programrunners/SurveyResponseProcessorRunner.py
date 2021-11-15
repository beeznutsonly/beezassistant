from configparser import ConfigParser

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.messagecommandprocessor.messagecommandprocessortools.testfeaturetools.FeatureTesterDAO import FeatureTesterDAO
from botapplicationtools.programs.surveyresponseprocessor import SurveyResponseProcessor
from botapplicationtools.programs.surveyresponseprocessor.RedditTools import RedditTools
from botapplicationtools.programs.surveyresponseprocessor.UserMessage import UserMessage
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory


class SurveyResponseProcessorRunner(ProgramRunner):

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
        super().__init__(
            redditInterfaceFactory,
            databaseConnectionFactory,
            "Survey Response Processor Runner"
        )
        self.__initializeProgramRunner(configReader)

    def __initializeProgramRunner(self, configReader: ConfigParser):

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

        self._userProfile = userProfile

        self.__subredditName = subredditName
        self.__userMessage = UserMessage(
            messageSubject,
            messageBody
        )
        self.__userFlairId = userFlairId
        self.__testingWindow = testingWindow

    def _runCore(self, redditInterface, connection):

        redditTools = RedditTools(
            redditInterface.getPrawReddit,
            self.__subredditName,
            self.__userFlairId
        )

        SurveyResponseProcessor.execute(
            redditTools,
            FeatureTesterDAO(
                connection
            ),
            self.__userMessage,
            self.__testingWindow
        )
