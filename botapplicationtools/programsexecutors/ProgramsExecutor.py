# -*- coding: utf-8 -*-

import logging
from abc import ABC, abstractmethod
from typing import Dict


class ProgramsExecutor(ABC):
    """
    Class responsible for executing programs
    """

    _isProgramsExecutorShutDown: bool
    _programsExecutorLogger: logging.Logger

    def __init__(self, programsExecutorName: str):
        self._programsExecutorLogger = logging.getLogger(
            programsExecutorName
        )
        self._isProgramsExecutorShutDown = False

    @abstractmethod
    def executeProgram(self, programCommand):
        """Execute the provided program command"""

        raise NotImplementedError

    @abstractmethod
    def getProgramStatuses(self) -> Dict[str, str]:
        """Get the executed program statuses"""

        raise NotImplementedError

    def shutDown(self, *args):
        """Shut down the programs executor"""

        self._isProgramsExecutorShutDown = True

    def isShutDown(self) -> bool:
        """Check if the Programs Executor is shut down"""

        return self._isProgramsExecutorShutDown

    def _informIfShutDown(self):
        """
        Convenience method to check shutdown status and log
        if programs executor is shut down
        """

        if self._isProgramsExecutorShutDown:
            self._programsExecutorLogger.warning(
                "The programs executor cannot execute any more programs "
                "after it has been shut down"
            )
