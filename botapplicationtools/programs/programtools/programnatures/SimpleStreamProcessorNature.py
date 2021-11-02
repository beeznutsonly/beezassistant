import time
from abc import ABC, abstractmethod
from collections import Generator
from typing import Callable

from prawcore.exceptions import RequestException, ServerError

from botapplicationtools.programs.programtools.programnatures.SimpleProgram import SimpleProgram


class SimpleStreamProcessorNature(SimpleProgram, ABC):
    """
    Class encapsulating a stream processor
    program nature
    """

    __stream: Generator
    __stopCondition: Callable

    def __init__(
            self,
            stream: Generator,
            stopCondition: Callable
    ):
        self.__stream = stream
        self.__stopCondition = stopCondition

    def execute(self):

        # Program loop
        while not self.__stopCondition():

            try:
                # "Comment listener" loop
                for streamItem in self.__stream:

                    # Handle "pause" token
                    if streamItem is None:

                        # Exit the loop if stop condition satisfied
                        if self.__stopCondition():
                            break

                        self._runPauseHandler()
                        continue

                    self._runNatureCore()

            # Handle if connection to the Reddit API is lost
            except (RequestException, ServerError):

                time.sleep(30)

    def _runPauseHandler(self, *args):
        """Execute when stream is paused"""
        pass

    @abstractmethod
    def _runNatureCore(self, *args):
        """Run core program"""

        raise NotImplementedError()
