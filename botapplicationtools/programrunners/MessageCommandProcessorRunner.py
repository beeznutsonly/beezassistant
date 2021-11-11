import json
from configparser import ConfigParser
from typing import List

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.messagecommandprocessor.MessageCommandProcessor import MessageCommandProcessor
from botapplicationtools.programs.messagecommandprocessor.messagecommandprocessortools.CommandProcessorFactory import \
    CommandProcessorFactory
from botapplicationtools.programs.programtools.featuretestertools.FeatureTesterDAO import FeatureTesterDAO
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory \
    import RedditInterfaceFactory


class MessageCommandProcessorRunner(ProgramRunner):
    """
    Class responsible for running multiple
    Message Command Processor instances
    """

    __commands: List[str]

    def __init__(
            self,
            redditInterfaceFactory: RedditInterfaceFactory,
            databaseConnectionFactory: DatabaseConnectionFactory,
            configReader: ConfigParser
    ):
        super().__init__(
            redditInterfaceFactory,
            databaseConnectionFactory,
            "Message Command Processor"
        )
        self.__initializeProgramRunner(configReader)

    def __initializeProgramRunner(self, configReader: ConfigParser):
        """Initialize the Message Command Processor Runner"""

        # Retrieving initial variable values from the config. reader
        section = "MessageCommandProcessor"
        userProfile = configReader.get(
            section, "userProfile"
        )
        commands = json.loads(
            configReader.get(
                section, "commands"
            )
        )

        # Instance variable initialization
        self._userProfile = userProfile
        self.__commands = commands

    def _runCore(self, redditInterface, connection):

        commandProcessors = CommandProcessorFactory.getCommandProcessors(
            self.__commands, connection
        )
        prawReddit = redditInterface.getPrawReddit
        featureTesterDAO = FeatureTesterDAO(connection)

        messageCommandProcessor = MessageCommandProcessor(
            commandProcessors,
            prawReddit,
            featureTesterDAO,
            self.isShutDown
        )

        messageCommandProcessor.execute()
