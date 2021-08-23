# -*- coding: utf-8 -*-

"""
Class responsible for running StarsArchiveWikiPageWriter 
program instances
"""

import logging
from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarView import IndividualStarView
from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarViewDAO import IndividualStarViewDAO
from botapplicationtools.programs.starsarchivewikipagewriter.StarsArchiveWikiPageWriter import StarsArchiveWikiPageWriter

class StarsArchiveWikiPageWriterRunner(ProgramRunner):

    __starsArchiveWikiPageWriterRunnerLogger : logging.Logger
    __isRunnerShutDown : bool

    __starsArchiveWikiPageWriterSubredditName : str
    __wikiPage = None
    __defaultStarViews : list
    __databaseConnectionFactory = None

    def __init__(
        self,
        starsArchiveWikiPageWriterSubredditName,
        wikiPage,
        defaultStarViews
    ):
        self.__starsArchiveWikiPageWriterRunnerLogger = \
            logging.getLogger("starsArchiveWikiPageWriterRunner")
        self.__starsArchiveWikiPageWriterSubredditName = \
            starsArchiveWikiPageWriterSubredditName
        self.__wikiPage = wikiPage
        self.__defaultStarViews = defaultStarViews
        self.__isRunnerShutDown = False

    
    def run(self):
        with self.__databaseConnectionFactory \
                .getConnection() \
                as databaseConnection:

            starsArchiveWikiPageWriter = \
                self.__getNewStarsArchiveWikiPageWriter(
                    databaseConnection, self.__defaultStarViews
                )

            # Executing the program
            self.__starsArchiveWikiPageWriterRunnerLogger.info(
                'Stars Archive Wiki Page Writer is now running'
            )
            starsArchiveWikiPageWriter.writeToWiki()
            self.__starsArchiveWikiPageWriterRunnerLogger.info(
                'Stars Archive Wiki Page Writer completed'
            )

    # Convenience method to return a new
    # StarsArchiveWikiPageWriter
    def __getNewStarsArchiveWikiPageWriter(
            self,
            databaseConnection,
            starViews=None
    ):

        if starViews is None:
            starViews = self.__defaultStarViews

        # Oh, just initializing the database connection
        databaseConnection = self.__programRunnerIO \
            .getDatabaseConnectionFactory() \
            .getConnection() \
            if databaseConnection is None \
            else databaseConnection

        # Generating the default Starview objects
        starViewObjects = []
        for starView in ([] if starViews is None else starViews):
            if starView == 'individual':
                starViewObjects.append(
                    IndividualStarView(
                        self.__starsArchiveWikiPageWriterSubredditName,
                        IndividualStarViewDAO(
                            databaseConnection
                        )
                    )
                )
            # If provided default starview is invalid
            else:
                self.__starsArchiveWikiPageWriterRunnerLogger.warning(
                    "'{}' is an invalid starview and shall"
                    " be removed from the list of provided"
                    " default starviews".format(starView)
                )

        # Use default Starviews if list of provided starviews is empty
        if len(starViewObjects) == 0:
            self.__starsArchiveWikiPageWriterRunnerLogger.warning(
                "No StarViews were loaded from the "
                "provided list so the default StarViews "
                "shall be used for the "
                "Stars Archive Wiki Page Writer."
            )

            # (Be careful you naughty, naughty boy)
            return self.__getNewStarsArchiveWikiPageWriter(
                databaseConnection, self.__defaultStarViews
            )

        return StarsArchiveWikiPageWriter(self.__wikiPage, starViewObjects)
