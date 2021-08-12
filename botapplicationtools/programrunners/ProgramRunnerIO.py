# -*- coding: utf-8 -*

"""
Class holding the I/O tools used by the ProgramRunner
"""


class ProgramRunnerIO:

    __configParser = None
    __databaseConnectionFactory = None

    def __init__(
            self,
            configParser,
            databaseConnectionFactory
    ):
        self.__configParser = configParser
        self.__databaseConnectionFactory = databaseConnectionFactory

    def getConfigParser(self):
        return self.__configParser

    def getDatabaseConnectionFactory(self):
        return self.__databaseConnectionFactory
