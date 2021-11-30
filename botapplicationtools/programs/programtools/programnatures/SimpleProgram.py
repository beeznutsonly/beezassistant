from abc import ABC, abstractmethod


class SimpleProgram(ABC):
    """Class representing a simple program"""

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute the program"""

        raise NotImplementedError()
