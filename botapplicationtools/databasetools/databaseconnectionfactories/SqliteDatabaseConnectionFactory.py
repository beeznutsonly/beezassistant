# -*- coding: utf-8 -*

import sqlite3

from os.path import isfile

from botapplicationtools.databasetools.exceptions.DatabaseConnectionFailureError import DatabaseConnectionFailureError
from botapplicationtools.databasetools.exceptions.DatabaseNotFoundError import DatabaseNotFoundError
from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory


class SqliteDatabaseConnectionFactory(DatabaseConnectionFactory):
    """
    Connection factory for Bot Application's sqlite database
    """

    __databaseString: str
    __isClosed: bool

    def __init__(self, databaseString):

        # Raise exception if database file is not found
        if not isfile(databaseString):
            raise DatabaseNotFoundError(
                "Database '{}' does not exist".format(databaseString)
            )

        self.__databaseString = databaseString
        self.__isClosed = False

    def getConnection(self):
        if self.__isClosed:
            raise DatabaseConnectionFailureError(
                "The connection factory is closed"
            )
        return sqlite3.connect(
            self.__databaseString,
            check_same_thread=False
        )

    def yieldConnection(self, connection):
        connection.close()

    def shutDown(self):
        self.__isClosed = True