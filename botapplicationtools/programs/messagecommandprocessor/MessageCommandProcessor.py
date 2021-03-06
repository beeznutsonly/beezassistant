from typing import Dict

from praw import Reddit
from praw.models import Message

from botapplicationtools.programs.messagecommandprocessor.commandprocessors.CommandProcessor import CommandProcessor
from botapplicationtools.programs.messagecommandprocessor \
    .messagecommandprocessortools.testfeaturetools.FeatureTesterDAO import FeatureTesterDAO
from botapplicationtools.programs.programtools.generaltools.Decorators import consumestransientapierrors
from botapplicationtools.programs.programtools.programnatures.streamprocessingnature.SimpleCustomStreamFactory import \
    SimpleCustomStreamFactory
from botapplicationtools.programs.programtools.programnatures.streamprocessingnature.SimpleStreamProcessorNature \
    import SimpleStreamProcessorNature


class MessageCommandProcessor(SimpleStreamProcessorNature):
    """Program to process message commands"""

    PROGRAM_NAME: str = "Message Command Processor"

    def __init__(
            self,
            commandProcessors: Dict[str, CommandProcessor],
            prawReddit: Reddit,
            featureTesterDAO: FeatureTesterDAO,
            stopCondition
    ):
        super().__init__(
            SimpleCustomStreamFactory(
                lambda: prawReddit.inbox.unread
            ),
            stopCondition,
            MessageCommandProcessor.PROGRAM_NAME
        )
        self.__commandProcessors = commandProcessors
        self.__featureTesterDAO = featureTesterDAO

    @consumestransientapierrors
    def _runNatureCore(self, unread):

        # Process if unread item is Message
        if isinstance(unread, Message):
            message: Message = unread

            # Process if message is message command
            if message.subject.startswith("!"):
                command = message.subject[1:]

                # Process if command is included in
                # provided commands
                if command in self.__commandProcessors.keys():
                    self._programLogger.debug(
                        'Processing message command "{}" with '
                        'arguments "{}" (Message ID: {})'.format(
                            command,
                            message.body,
                            message.id
                        )
                    )
                    self.__commandProcessors[command].processMessage(
                        message,
                        featureTesterDAO=self.__featureTesterDAO
                    )
