# -*- coding: utf-8 -*-
import json
from configparser import ConfigParser
from typing import List

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory \
    import DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.programtools.starprofiletools.StarDAO import StarDAO
from botapplicationtools.programs.programtools.starprofiletools.StarLinkDAO import StarLinkDAO
from botapplicationtools.programs.starinforeplyer.StarInfoReplyer import StarInfoReplyer
from botapplicationtools.programs.starinforeplyer.CustomAddenda import CustomAddenda
from botapplicationtools.programs.starinforeplyer.RedditTools import RedditTools
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerCommentedDAO \
    import StarInfoReplyerCommentedDAO
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerExcludedDAO \
    import StarInfoReplyerExcludedDAO
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerIO import StarInfoReplyerIO
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerStorage \
    import StarInfoReplyerStorage
from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetailDAO \
    import StarSceneInfoSubmissionDetailDAO
from botapplicationtools.programs.starinforeplyer.StarStorage import StarStorage
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory \
    import RedditInterfaceFactory


class StarInfoReplyerRunner(ProgramRunner):
    """
    Class responsible for running multiple
    StarInfoReplyer program instances
    """

    __groupsRefreshInterval: int
    __subreddits: List[str]
    __excludedUsers: List[str]
    __customAddenda: CustomAddenda

    def __init__(
            self,
            redditInterfaceFactory: RedditInterfaceFactory,
            databaseConnectionFactory: DatabaseConnectionFactory,
            configReader: ConfigParser
    ):
        super().__init__(
            redditInterfaceFactory,
            databaseConnectionFactory,
            "Star Info Replyer Runner"
        )
        self.__initializeProgramRunner(configReader)

    def __initializeProgramRunner(self, configReader):
        """Initializing the Star Info Replyer Runner"""

        # Retrieving values from configuration file

        section = 'StarInfoReplyerRunner'
        subreddits = json.loads(configReader.get(
            section, "subreddits"
        ))
        excludedUsers = json.loads(configReader.get(
            section, "excludedUsers"
        ))
        submissionSummaryAddendum = configReader.get(
            section, "submissionSummaryAddendum"
        )
        replyFooter = configReader.get(
            section, "replyFooter"
        )
        groupsRefreshInterval = configReader.getint(
            section, "groupsRefreshInterval"
        )
        userProfile = configReader.get(
            section, "userProfile"
        )

        # Setting up relevant instance variables

        self.__subreddits = subreddits
        self.__excludedUsers = excludedUsers
        self.__customAddenda = CustomAddenda(
            bytes(
                submissionSummaryAddendum,
                "utf-8"
            ).decode("unicode_escape"),
            bytes(
                replyFooter, "utf-8"
            ).decode("unicode_escape")
        )
        self.__groupsRefreshInterval = groupsRefreshInterval
        self._userProfile = userProfile

    def _runCore(self, redditInterface, connection):

        # Setting up the Replyer's Reddit Tools
        prawReddit = redditInterface.getPrawReddit
        redditTools = RedditTools(
            prawReddit,
            self.__subreddits,
            self.__excludedUsers
        )

        # Storage tools for the StarInfoReplyer
        starInfoReplyerCommentedDAO = StarInfoReplyerCommentedDAO(
            connection
        )
        starInfoReplyerExcludedDAO = StarInfoReplyerExcludedDAO(
            connection
        )
        starSceneInfoSubmissionDetailDAO = StarSceneInfoSubmissionDetailDAO(
            connection
        )
        starDAO = StarDAO(connection)
        starLinkDAO = StarLinkDAO(connection)

        starInfoReplyerIO = StarInfoReplyerIO(
            StarInfoReplyerStorage(
                starInfoReplyerCommentedDAO,
                starInfoReplyerExcludedDAO,
                starSceneInfoSubmissionDetailDAO,
                StarStorage(starDAO, starLinkDAO)
            ),
            redditTools
        )

        # Executing the program
        starInfoReplyer = StarInfoReplyer(
            starInfoReplyerIO,
            self.__groupsRefreshInterval,
            self.isShutDown,
            self.__customAddenda
        )
        starInfoReplyer.execute()
