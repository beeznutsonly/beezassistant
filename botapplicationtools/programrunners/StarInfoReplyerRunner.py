# -*- coding: utf-8 -*-
import json
from typing import List

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.starinforeplyer import StarInfoReplyer
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerCommentedDAO import StarInfoReplyerCommentedDAO
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerStorage import StarInfoReplyerStorage
from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarViewDAO import IndividualStarViewDAO
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory


class StarInfoReplyerRunner(ProgramRunner):
    """
    Class responsible for running multiple
    SceneInfoArchiver program instances
    """

    __databaseConnectionFactory: DatabaseConnectionFactory
    __redditInterfaceFactory: RedditInterfaceFactory

    __refreshInterval: int
    __subreddits: List[str]

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
            "Retrieving Program Runner initial values from the config. reader"
        )
        section = 'StarInfoReplyerRunner'
        subreddits = json.loads(configReader.get(
            section, "subreddits"
        ))
        refreshInterval = configReader.getint(
            section, "refreshInterval"
        )

        # Setting up relevant instance variables

        self.__subreddits = subreddits
        self.__refreshInterval = refreshInterval

    def run(self):
        """Execute the Star Info Replyer"""

        prawReddit = self.__redditInterfaceFactory \
            .getRedditInterface() \
            .getPrawReddit
        commentStream = prawReddit.subreddit(
            '+'.join(self.__subreddits)
        ).stream.comments(pause_after=0)

        with self.__databaseConnectionFactory.getConnection() \
                as connection:

            starInfoReplyerCommentedDAO = StarInfoReplyerCommentedDAO(
                connection
            )

            individualStarViewDAO = IndividualStarViewDAO(
                connection
            )

            StarInfoReplyer.execute(
                commentStream,
                StarInfoReplyerStorage(
                    starInfoReplyerCommentedDAO,
                    individualStarViewDAO
                ),
                self.__refreshInterval,
                self.isShutDown
            )
