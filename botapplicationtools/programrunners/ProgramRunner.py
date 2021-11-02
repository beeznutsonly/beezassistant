# -*- coding: utf-8 -*-

import logging
from abc import ABC, abstractmethod

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programs.programtools.generaltools.RedditInterface import RedditInterface
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory


class ProgramRunner(ABC):
    """
    Class responsible for running multiple
    instances of a specific program
    """

    _redditInterfaceFactory: RedditInterfaceFactory
    _databaseConnectionFactory: DatabaseConnectionFactory
    _programRunnerName: str
    _programRunnerLogger: logging.Logger
    _userProfile: str
    _isProgramRunnerShutDown: bool

    def __init__(
            self,
            redditInterfaceFactory: RedditInterfaceFactory,
            databaseConnectionFactory: DatabaseConnectionFactory,
            programRunnerName: str,
            userProfile: str = None
    ):
        self._redditInterfaceFactory = redditInterfaceFactory
        self._databaseConnectionFactory = databaseConnectionFactory
        self._programRunnerName = programRunnerName
        self._programRunnerLogger = logging.getLogger(
            programRunnerName
        )
        self._userProfile = userProfile
        self._isProgramRunnerShutDown = False

    def run(self):
        """Run a new program instance"""

        # Quick shutdown check before proceeding
        if self.__informIfShutDown():
            return

        programRunnerLogger = self._programRunnerLogger

        # Running the program
        try:

            programRunnerLogger.info('{} is now running'.format(
                self._programRunnerName
            ))

            with self._databaseConnectionFactory.getConnection() \
                    as connection:

                # Run the core instructions of the program runner
                self._runCore(
                    self._redditInterfaceFactory.getRedditInterface(
                        self._userProfile
                    ),
                    connection
                )

                # Completion message determination
                if self.isShutDown():
                    programRunnerLogger.info(
                        "{} successfully shut down".format(
                            self._programRunnerName
                        )
                    )
                else:
                    programRunnerLogger.info(
                        "{} Completed".format(
                            self._programRunnerName
                        )
                    )

        # Handle in the event of a program crash
        except Exception as ex:
            programRunnerLogger.error(
                "A terminal error occurred while running the {} : "
                .format(self._programRunnerName) +
                str(ex.args),
                exc_info=True
            )

        finally:
            # Dispose of database connection
            self._databaseConnectionFactory.yieldConnection(
                connection
            )

    @abstractmethod
    def _runCore(self, redditInterface: RedditInterface, connection):
        """Run the core instructions of the program runner"""
        raise NotImplementedError()

    def isShutDown(self) -> bool:
        """Check if Program Runner is shut down"""
        return self._isProgramRunnerShutDown

    def shutDown(self):
        """Shut down the Program Runner"""
        self._isProgramRunnerShutDown = True

    def __informIfShutDown(self):
        """
        Convenience method to check shutdown status and log
        if program runner is shut down
        """

        if self.isShutDown():
            self._programRunnerLogger.warning(
                "The program runner cannot run any more program "
                "instances after it has been shut down"
            )

        return self.isShutDown()
