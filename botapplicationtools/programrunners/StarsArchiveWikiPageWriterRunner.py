# -*- coding: utf-8 -*-

"""
Class responsible for running StarsArchiveWikiPageWriter 
program instances
"""
import json
import logging
from typing import List

import praw.models

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.GenericProgramRunner import GenericProgramRunner
from botapplicationtools.programs.starsarchivewikipagewriter import StarsArchiveWikiPageWriter, StarViewFactory
from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarView import IndividualStarView


class StarsArchiveWikiPageWriterRunner(GenericProgramRunner):

    __starsArchiveWikiPageWriterRunnerLogger: logging.Logger
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

        self.__starsArchiveWikiPageWriterRunnerLogger = \
            logging.getLogger("starsArchiveWikiPageWriterRunner")
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__initializeStarsArchiveWikiPageWriterRunner(
            redditInterface.getPrawReddit(), configReader
        )

    def __initializeStarsArchiveWikiPageWriterRunner(
            self, prawReddit, configReader
    ):

        # Loading values from configuration file
        # -------------------------------------------------------------------------------

        self.__starsArchiveWikiPageWriterRunnerLogger.debug(
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

        self.__starsArchiveWikiPageWriterRunnerLogger.debug(
            "Initializing Stars Archive Wiki Page Writer variables"
        )

        # Initializing default starviews
        validStarViewList = []
        for defaultStarView in defaultStarViews:
            if defaultStarView == 'individual':
                validStarViewList.append(
                    defaultStarView
                )

            # If provided default star view is invalid
            else:
                self.__starsArchiveWikiPageWriterRunnerLogger.warning(
                    "'{}' is an invalid Star view and shall"
                    " be removed from the list of provided"
                    " default starviews".format(defaultStarView)
                )

        # Use default Starviews if list of provided starviews is empty
        if len(validStarViewList) == 0:
            validStarViewList.extend(['individual'])
            self.__starsArchiveWikiPageWriterRunnerLogger.warning(
                "No initial Star views were loaded so the following "
                "default Star views shall be used for the "
                "Stars Archive Wiki Page Writer: {}".format(
                    str(validStarViewList)
                )
            )
        self.__defaultStarViews = validStarViewList

        self.__wikiPage = prawReddit \
            .subreddit(starsArchiveWikiPageWriterSubredditName) \
            .wiki[wikiName]

    def run(self):

        # First confirm that the program runner is not shutdown
        if self.__informIfShutdown():
            return

        programRunnerLogger = \
            self.__starsArchiveWikiPageWriterRunnerLogger

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

    def __informIfShutdown(self):
        return self.isShutDown()
