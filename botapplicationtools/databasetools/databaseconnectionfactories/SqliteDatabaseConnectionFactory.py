# -*- coding: utf-8 -*

"""
Connection factory for Bot Application's sqlite database
"""
import logging
import sqlite3

from os.path import isfile


class SqliteDatabaseConnectionFactory:

    __databaseString = None

    def __init__(self, databaseString):

        logging.getLogger()

        # Raise exception if database file is not found
        if not isfile(databaseString):
            raise FileNotFoundError(
                "Database '{}' does not exist".format(databaseString)
            )

        self.__databaseString = databaseString

    def getConnection(self):
        return sqlite3.connect(self.__databaseString, check_same_thread=False)

    def __getConnection(databaseString):
        return sqlite3.connect(databaseString)