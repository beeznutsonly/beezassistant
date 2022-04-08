from abc import ABC, abstractmethod
from collections import Generator


class StreamFactory(ABC):
    """
    Class responsible for producing
    new Reddit Object streams at request
    """

    @abstractmethod
    def getNewStream(self) -> Generator:
        """Produce new stream"""

        raise NotImplementedError()
