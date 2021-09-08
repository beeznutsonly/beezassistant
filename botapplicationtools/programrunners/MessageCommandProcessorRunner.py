from configparser import ConfigParser

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.messagecommandprocessor import MessageCommandProcessor
from botapplicationtools.programs.messagecommandprocessor.commandprocessors \
    .StarInfoReplyerCommandProcessor import StarInfoReplyerCommandProcessor
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerExcludedDAO \
    import StarInfoReplyerExcludedDAO
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory \
    import RedditInterfaceFactory


class MessageCommandProcessorRunner(ProgramRunner):

    __databaseConnectionFactory: DatabaseConnectionFactory
    __redditInterfaceFactory: RedditInterfaceFactory

    def __init__(
            self,
            databaseConnectionFactory:
            DatabaseConnectionFactory,

            redditInterfaceFactory:
            RedditInterfaceFactory,

            configReader: ConfigParser
    ):
        super().__init__()
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__redditInterfaceFactory = redditInterfaceFactory

    def run(self):

        if self._informIfShutDown():
            return

        self._programRunnerLogger.info(
            "Message Command Processor is now running."
        )

        prawReddit = self.__redditInterfaceFactory \
            .getRedditInterface() \
            .getPrawReddit

        with self.__databaseConnectionFactory.getConnection() as \
                databaseConnection:
            starInfoReplyerExcludedDAO = StarInfoReplyerExcludedDAO(
                databaseConnection
            )
            messageCommands = {
                "StarInfoReplyer": StarInfoReplyerCommandProcessor(
                    starInfoReplyerExcludedDAO
                )
            }
            MessageCommandProcessor.execute(
                messageCommands, prawReddit, self.isShutDown
            )

        self.__databaseConnectionFactory.yieldConnection(
            databaseConnection
        )
        if self.isShutDown():
            self._programRunnerLogger.info(
                "Message Command Processor successfully shut down."
            )
        else:
            self._programRunnerLogger.info(
                "Message Command Processor completed."
            )
