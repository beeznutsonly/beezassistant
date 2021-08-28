from abc import ABC, abstractmethod


class DatabaseConnectionFactory(ABC):

    @abstractmethod
    def getConnection(self):
        pass
