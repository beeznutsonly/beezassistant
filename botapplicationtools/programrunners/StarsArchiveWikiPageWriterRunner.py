# -*- coding: utf-8 -*-

import json
from configparser import ConfigParser
from typing import List

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.starsarchivewikipagewriter import StarsArchiveWikiPageWriter, StarViewFactory
from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarView import IndividualStarView
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory


class StarsArchiveWikiPageWriterRunner(ProgramRunner):
    """
    Class responsible for running StarsArchiveWikiPageWriter 
    program instances
    """

    __wikiName: str
    __subredditName: str
    # TODO: Replace generic with StarView
    __defaultStarViews: List[IndividualStarView]

    def __init__(
            self,
            redditInterfaceFactory: RedditInterfaceFactory,
            databaseConnectionFactory: DatabaseConnectionFactory,
            configReader: ConfigParser
    ):
        super(StarsArchiveWikiPageWriterRunner, self).__init__(
            redditInterfaceFactory,
            databaseConnectionFactory,
            "Stars Archive Wiki Page Writer Runner"
        )
        self.__initializeProgramRunner(
            configReader
        )

    def __initializeProgramRunner(
            self, configReader
    ):
        """Initializing the Stars Archive Wiki Page Writer"""

        # Retrieving values from configuration file
        # -------------------------------------------------------------------------------

        section = 'StarsArchiveWikiPageWriterRunner'
        subredditName = configReader.get(
            section, 'subredditName'
        )
        wikiName = configReader.get(
            section, 'wikiName'
        )
        defaultStarViews = json.loads(configReader.get(
            section, 'defaultStarViews'
        ))
        userProfile = configReader.get(
            section, "userProfile"
        )

        # Instance variable initialization
        # -------------------------------------------------------------------------------

        self._programRunnerLogger.debug(
            "Initializing Stars Archive Wiki Page Writer variables"
        )

        self.__userProfile = userProfile
        self.__subredditName = subredditName
        self.__wikiName = wikiName
        # TODO: Do something about this absolute garbage
        # Setting up default StarViews
        validStarViewList = []
        for defaultStarView in defaultStarViews:
            if defaultStarView == 'individual':
                validStarViewList.append(
                    defaultStarView
                )

            # If provided default star view is invalid
            else:
                self._programRunnerLogger.warning(
                    "'{}' is an invalid Star view and shall"
                    " be removed from the list of provided"
                    " default starviews".format(defaultStarView)
                )

        # Use default StarViews if list of provided StarViews is empty
        if len(validStarViewList) == 0:
            validStarViewList.extend(['individual'])
            self._programRunnerLogger.warning(
                "No initial Star views were loaded so the following "
                "default Star views shall be used for the "
                "Stars Archive Wiki Page Writer: {}".format(
                    str(validStarViewList)
                )
            )
        self.__defaultStarViews = validStarViewList

    def _runCore(self, redditInterface, connection):

        wikiPage = redditInterface \
            .getPrawReddit \
            .subreddit(self.__subredditName) \
            .wiki[self.__wikiName]

        starViewObjects = StarViewFactory.getStarViews(
            connection, self.__defaultStarViews
        )
        StarsArchiveWikiPageWriter.execute(
            wikiPage, starViewObjects
        )
