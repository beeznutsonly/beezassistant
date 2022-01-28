from abc import ABC, abstractmethod
from collections import Generator


class StreamFactory(ABC):
    """"""

    @abstractmethod
    def getNewStream(self) -> Generator:
        raise NotImplementedError()
