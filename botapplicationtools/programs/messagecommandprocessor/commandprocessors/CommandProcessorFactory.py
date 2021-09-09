from typing import List

from botapplicationtools.programs.messagecommandprocessor.commandprocessors \
    .StarInfoReplyerCommandProcessor import StarInfoReplyerCommandProcessor
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerExcludedDAO \
    import StarInfoReplyerExcludedDAO


class CommandProcessorFactory:
    """Class responsible for generating CommandProcessors"""

    @classmethod
    def getCommandProcessor(cls, command: str, databaseConnection):
        """Retrieve the command processor for the corresponding command"""

        # For StarInfoReplyer command
        if command == "StarInfoReplyer":
            return StarInfoReplyerCommandProcessor(
                StarInfoReplyerExcludedDAO(
                    databaseConnection
                )
            )
        # Handle for unknown command
        else:
            return None

    @classmethod
    def getCommandProcessors(cls, commands: List[str], databaseConnection):
        """Retrieve the command processors for the provided commands"""

        commandProcessors = {}
        for command in commands:
            # Return the command processor for each
            # provided command
            commandProcessor = cls.getCommandProcessor(
                command, databaseConnection
            )
            if commandProcessor is not None:
                # Append to collection of command processors
                # if command processor returned
                commandProcessors[command] = commandProcessor

        return commandProcessors