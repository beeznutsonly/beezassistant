import json
from configparser import ConfigParser

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.messagecommandprocessor import MessageCommandProcessor
from botapplicationtools.programs.messagecommandprocessor.commandprocessors.CommandProcessorFactory import \
    CommandProcessorFactory
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory \
    import RedditInterfaceFactory


class MessageCommandProcessorRunner(ProgramRunner):
    """
    Class responsible for running multiple
    Message Command Processor instances
    """

    __databaseConnectionFactory: DatabaseConnectionFactory
    __redditInterfaceFactory: RedditInterfaceFactory
    __userProfile: str

    __commands = None

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
        self.__initializeProgramRunner(configReader)

    def __initializeProgramRunner(self, configReader: ConfigParser):
        """Initialize the Message Command Processor Runner"""

        self._programRunnerLogger.info(
            "Initializing Message Command Processor Runner variables"
        )

        # Retrieving initial variable values from the config. reader
        section = "MessageCommandProcessor"
        commands = json.loads(
            configReader.get(
                section, "commands"
            )
        )
        userProfile = configReader.get(
            section, "userProfile"
        )

        # Instance variable initialization
        self.__commands = commands
        self.__userProfile = userProfile

    def run(self):

        # Quick shutdown check before proceeding
        if self._informIfShutDown():
            return

        try:

            # Executing the program
            self._programRunnerLogger.info(
                "Message Command Processor is now running."
            )
            prawReddit = self.__redditInterfaceFactory \
                .getRedditInterface(self.__userProfile) \
                .getPrawReddit

            with self.__databaseConnectionFactory.getConnection() as \
                    databaseConnection:

                messageCommands = CommandProcessorFactory.getCommandProcessors(
                    self.__commands, databaseConnection
                )
                MessageCommandProcessor.execute(
                    messageCommands, prawReddit, self.isShutDown
                )

            if self.isShutDown():
                self._programRunnerLogger.info(
                    "Message Command Processor successfully shut down."
                )
            else:
                self._programRunnerLogger.info(
                    "Message Command Processor completed."
                )

        # Handle if an error occurs while running the Message Command Processor
        except Exception as er:
            self._programRunnerLogger.error(
                "A terminal error occurred while running the Message "
                "Command Processor: " + str(er.args), exc_info=True
            )
        finally:
            # Disposing of database connection
            # once program is done executing
            self.__databaseConnectionFactory.yieldConnection(
                databaseConnection
            )
