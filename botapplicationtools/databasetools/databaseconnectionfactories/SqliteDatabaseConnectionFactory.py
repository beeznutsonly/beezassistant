# -*- coding: utf-8 -*

"""
Connection factory for Bot Application's sqlite database
"""

import sqlite3

from os.path import isfile

from botapplicationtools.databasetools.exceptions.DatabaseNotFoundError import DatabaseNotFoundError
from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory


class SqliteDatabaseConnectionFactory(DatabaseConnectionFactory):

    __databaseString = None

    def __init__(self, databaseString):

        # Raise exception if database file is not found
        if not isfile(databaseString):
            raise DatabaseNotFoundError(
                "Database '{}' does not exist".format(databaseString)
            )

        self.__databaseString = databaseString

    def getConnection(self):
        return sqlite3.connect(self.__databaseString, check_same_thread=False)

