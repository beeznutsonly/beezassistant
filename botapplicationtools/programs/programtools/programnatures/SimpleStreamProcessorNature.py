from abc import ABC
from collections import Generator
from typing import Callable

from botapplicationtools.programs.programtools.generaltools.Decorators import consumestransientapierrors
from botapplicationtools.programs.programtools.programnatures.RecurringProgramNature import RecurringProgramNature


class SimpleStreamProcessorNature(RecurringProgramNature, ABC):
    """
    Class encapsulating a stream processor
    program nature
    """

    def __init__(
            self,
            stream: Generator,
            stopCondition: Callable[..., bool]
    ):
        super().__init__(stopCondition)
        self.__stream = stream

    def execute(self, *args, **kwargs):

        # "Comment listener" loop
        for streamItem in self.__stream:

            # Handle "pause" token
            if streamItem is None:

                # Exit the loop if stop condition satisfied
                if self.__stopCondition():
                    break

                self._runPauseHandler()
                continue

            self._runNatureCore(streamItem)

    @consumestransientapierrors
    def _runNatureCore(self, *args, **kwargs):
        super()._runNatureCore(*args, **kwargs)

    def _runPauseHandler(self, *args):
        """Execute when stream is paused"""
        pass
