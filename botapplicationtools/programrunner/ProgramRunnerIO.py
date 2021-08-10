# -*- coding: utf-8 -*

"""
Class holding the I/O tools used by the ProgramRunner
"""


class ProgramRunnerIO:

    __configParser = None
    __programRunnerLogger = None
    __databaseConnectionFactory = None

    def __init__(
            self,
            configParser,
            programRunnerLogger,
            databaseConnectionFactory
    ):
        self.__configParser = configParser
        self.__programRunnerLogger = programRunnerLogger
        self.__databaseConnectionFactory = databaseConnectionFactory

    def getConfigParser(self):
        return self.__configParser

    def getProgramRunnerLogger(self):
        return self.__programRunnerLogger

    def getDatabaseConnectionFactory(self):
        return self.__databaseConnectionFactory
