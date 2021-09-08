# -*- coding: utf-8 -*

from abc import ABC, abstractmethod


class DatabaseConnectionFactory(ABC):
    """Factory class for database connections"""

    @abstractmethod
    def getConnection(self):
        """Retrieve a database connection"""

        raise NotImplementedError

    @abstractmethod
    def yieldConnection(self, connection):
        """
        Return connection to connection factory when
        finished using it
        """

        raise NotImplementedError
