# -*- coding: utf-8 -*-
import json
from typing import List

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory \
    import DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.starinforeplyer import StarInfoReplyer
from botapplicationtools.programs.starinforeplyer.RedditTools import RedditTools
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerCommentedDAO \
    import StarInfoReplyerCommentedDAO
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerIO import StarInfoReplyerIO
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerStorage \
    import StarInfoReplyerStorage
from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetailDAO \
    import StarSceneInfoSubmissionDetailDAO
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory \
    import RedditInterfaceFactory


class StarInfoReplyerRunner(ProgramRunner):
    """
    Class responsible for running multiple
    StarInfoReplyer program instances
    """

    __databaseConnectionFactory: DatabaseConnectionFactory
    __redditInterfaceFactory: RedditInterfaceFactory

    __groupsRefreshInterval: int
    __subreddits: List[str]
    __excludedUsers: List[str]
    __replyFooter: str

    def __init__(
            self,
            databaseConnectionFactory,
            redditInterfaceFactory,
            configReader
    ):
        super().__init__()
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__redditInterfaceFactory = redditInterfaceFactory
        self.__initializeStarInfoReplyerRunner(configReader)

    def __initializeStarInfoReplyerRunner(self, configReader):
        """Initializing the Star Info Replyer Runner"""

        # Retrieving values from configuration file

        self._programRunnerLogger.debug(
            "Retrieving Star Info Replyer Runner initial "
            "values from the config. reader"
        )
        section = 'StarInfoReplyerRunner'
        subreddits = json.loads(configReader.get(
            section, "subreddits"
        ))
        excludedUsers = json.loads(configReader.get(
            section, "excludedUsers"
        ))
        replyFooter = str(configReader.get(
            section, "replyFooter"
        ))
        groupsRefreshInterval = configReader.getint(
            section, "groupsRefreshInterval"
        )

        # Setting up relevant instance variables

        self.__subreddits = subreddits
        self.__excludedUsers = excludedUsers
        self.__replyFooter = bytes(
            replyFooter, "utf-8"
        ).decode("unicode_escape")
        self.__groupsRefreshInterval = groupsRefreshInterval

    def run(self):
        """Execute the Star Info Replyer"""

        # First confirm that the program runner is not shutdown
        if self._informIfShutDown():
            return

        programRunnerLogger = self._programRunnerLogger

        try:

            # Executing the program
            programRunnerLogger.info('Star Info Replyer is now running')

            # Setting up the Replyer's Reddit Tools
            prawReddit = self.__redditInterfaceFactory \
                .getRedditInterface() \
                .getPrawReddit
            redditTools = RedditTools(
                prawReddit,
                self.__subreddits,
                self.__excludedUsers
            )

            with self.__databaseConnectionFactory.getConnection() \
                    as connection:

                # Storage tools for the StarInfoReplyer
                starInfoReplyerCommentedDAO = StarInfoReplyerCommentedDAO(
                    connection
                )
                starSceneInfoSubmissionDetailDAO = StarSceneInfoSubmissionDetailDAO(
                    connection
                )

                starInfoReplyerIO = StarInfoReplyerIO(
                    StarInfoReplyerStorage(
                        starInfoReplyerCommentedDAO,
                        starSceneInfoSubmissionDetailDAO
                    ),
                    redditTools
                )

                # Executing the program
                StarInfoReplyer.execute(
                    starInfoReplyerIO,
                    self.__groupsRefreshInterval,
                    self.isShutDown,
                    self.__replyFooter
                )
            
            # Program termination message determination
            if self.isShutDown():
                programRunnerLogger.info(
                    'Star Info Replyer successfully shut down'
                )
            else:
                programRunnerLogger.info(
                    'Star Info Replyer completed'
                )
        
        # Handle if an error occurs while running the Star Info Replyer
        except Exception as er:
            programRunnerLogger.error(
                "A terminal error occurred while running the Star "
                "Info Replyer: " + str(er.args), exc_info=True
            )
