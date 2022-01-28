from abc import ABC
from typing import Callable

from botapplicationtools.programs.programtools.generaltools.Decorators import consumestransientapierrors
from botapplicationtools.programs.programtools.programnatures.RecurringProgramNature import RecurringProgramNature
from botapplicationtools.programs.programtools.programnatures.streamprocessingnature.StreamFactory import StreamFactory


class SimpleStreamProcessorNature(RecurringProgramNature, ABC):
    """
    Class encapsulating a stream processor
    program nature
    """

    def __init__(
            self,
            streamFactory: StreamFactory,
            stopCondition: Callable[..., bool],
            programName: str
    ):
        super().__init__(programName, stopCondition)
        self.__streamFactory = streamFactory

    @consumestransientapierrors
    def execute(self, *args, **kwargs):

        # In case we somehow run out of
        # new items in the stream (IYKYK)
        while not self._stopCondition():

            stream = self.__streamFactory.getNewStream()

            # "New item listener" loop
            for streamItem in stream:

                # Handle "pause" token
                if streamItem is None:

                    # Exit the loop if stop condition satisfied
                    if self._stopCondition():
                        break

                    self._runPauseHandler()
                    continue

                self._runNatureCore(streamItem)

    def _runPauseHandler(self, *args):
        """Execute when stream is paused"""
        pass
