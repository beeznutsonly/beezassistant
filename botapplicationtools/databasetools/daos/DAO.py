# -*- coding: utf-8 -*

from abc import ABC


class DAO(ABC):
    """Class representing a generic Data Access Object"""

    _connection = None

    def __init__(self, connection):
        self._connection = connection

    def closeDAO(self):
        """Close the DAO"""

        if self._connection:
            self._connection.close()
