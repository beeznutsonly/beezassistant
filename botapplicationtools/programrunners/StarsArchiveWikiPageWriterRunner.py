# -*- coding: utf-8 -*-

import json
from typing import List

import praw.models

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.GenericProgramRunner import GenericProgramRunner
from botapplicationtools.programs.starsarchivewikipagewriter import StarsArchiveWikiPageWriter, StarViewFactory
from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarView import IndividualStarView


class StarsArchiveWikiPageWriterRunner(GenericProgramRunner):
    """
    Class responsible for running StarsArchiveWikiPageWriter 
    program instances
    """
    
    __databaseConnectionFactory: DatabaseConnectionFactory

    __wikiPage: praw.models.WikiPage
    # TODO: Replace generic with StarView
    __defaultStarViews: List[IndividualStarView]

    def __init__(
            self,
            databaseConnectionFactory,
            redditInterface,
            configReader
    ):
        super(StarsArchiveWikiPageWriterRunner, self).__init__()
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__initializeStarsArchiveWikiPageWriterRunner(
            redditInterface.getPrawReddit, configReader
        )

    def __initializeStarsArchiveWikiPageWriterRunner(
            self, prawReddit, configReader
    ):
        """Initializing the Stars Archive Wiki Page Writer"""

        # Retrieving values from configuration file
        # -------------------------------------------------------------------------------

        self._programRunnerLogger.debug(
            "Retrieving Program Runner initial values from the config. reader"
        )

        section = 'StarsArchiveWikiPageWriter'
        starsArchiveWikiPageWriterSubredditName = configReader.get(
            section, 'subredditName'
        )
        wikiName = configReader.get(
            section, 'wikiName'
        )
        defaultStarViews = json.loads(configReader.get(
            section, 'defaultStarViews'
        ))

        # Instance variable initialization
        # -------------------------------------------------------------------------------

        self._programRunnerLogger.debug(
            "Initializing Stars Archive Wiki Page Writer variables"
        )

        self.__wikiPage = prawReddit \
            .subreddit(starsArchiveWikiPageWriterSubredditName) \
            .wiki[wikiName]
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

    def run(self):

        # First confirm that the program runner is not shutdown
        if self._informIfShutDown():
            return

        programRunnerLogger = \
            self._programRunnerLogger

        with self.__databaseConnectionFactory.getConnection() \
                as databaseConnection:

            starViewObjects = StarViewFactory.getStarViews(
                databaseConnection, self.__defaultStarViews
            )

        # Executing the program
        programRunnerLogger.info(
            'Stars Archive Wiki Page Writer is now running'
        )
        StarsArchiveWikiPageWriter.execute(
            self.__wikiPage, starViewObjects
        )
        programRunnerLogger.info(
            'Stars Archive Wiki Page Writer completed'
        )
        
