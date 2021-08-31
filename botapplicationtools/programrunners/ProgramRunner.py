# -*- coding: utf-8 -*-

import logging
from abc import ABC, abstractmethod


class ProgramRunner(ABC):
    """
    Class responsible for running multiple
    instances of a specific program
    """

    _programRunnerLogger: logging.Logger
    _isProgramRunnerShutDown: bool

    def __init__(self):
        self._programRunnerLogger = logging.getLogger(
            __name__
        )
        self._isProgramRunnerShutDown = False

    @abstractmethod
    def run(self):
        """Run the program"""
        raise NotImplementedError()

    def isShutDown(self) -> bool:
        """Check if Program Runner is shut down"""
        return self._isProgramRunnerShutDown

    def shutDown(self):
        """Shut down the Program Runner"""
        self._isProgramRunnerShutDown = True

    def _informIfShutDown(self):
        """
        Convenience method to check shutdown status and log
        if program runner is shut down
        """

        if self._isProgramRunnerShutDown:
            self._programRunnerLogger.warning(
                "The program runner cannot run any more program "
                "instances after it has been shut down"
            )
