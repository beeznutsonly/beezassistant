import logging
from abc import ABC, abstractmethod


class SimpleProgram(ABC):
    """Class representing a simple program"""

    def __init__(self, programName: str):
        self._programLogger = logging.getLogger(
            programName
        )

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute the program"""

        raise NotImplementedError()
