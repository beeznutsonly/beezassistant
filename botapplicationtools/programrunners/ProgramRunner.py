# -*- coding: utf-8 -*-

"""
Class responsible for running the bot's programs
"""

import json
import logging
import re
import time
from datetime import datetime, timedelta

from botapplicationtools.programrunners.exceptions.ProgramRunnerInitializationError import \
    ProgramRunnerInitializationError
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoDAO import SceneInfoDAO
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmissionDAO import \
    SceneInfoSubmissionDAO
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmissionWithSceneInfoDAO import \
    SceneInfoSubmissionWithSceneInfoDAO
from botapplicationtools.programs.sceneinfostoragearchiver.Extractors import Extractors
from botapplicationtools.programs.sceneinfostoragearchiver import SceneInfoStorageArchiver
from botapplicationtools.programs.sceneinfostoragearchiver.SceneInfoSubmissionsWithSceneInfoStorage import \
    SceneInfoSubmissionsWithSceneInfoStorage
from botapplicationtools.programs.sceneinfostoragearchiver.SubredditSearchParameters import \
    SubredditSearchParameters
from botapplicationtools.programs.starsarchivewikipagewriter.StarsArchiveWikiPageWriter import \
    StarsArchiveWikiPageWriter
from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarView import IndividualStarView
from botapplicationtools.programs.starsarchivewikipagewriter.IndividualStarViewDAO import \
    IndividualStarViewDAO


class ProgramRunner:

    # Program Runner Initialization
    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------

    # Program Runner variables
    __isProgramRunnerShutdown = None
    __programRunnerIO = None
    __redditInterface = None
    __programRunnerLogger: logging.Logger

    def __init__(self, programRunnerIO, redditInterface):
        self.__programRunnerIO = programRunnerIO
        self.__redditInterface = redditInterface
        self.__initializeProgramRunner()

    # Scene Info Archiver variables
    __sceneInfoArchiverRefreshInterval = None
    __subredditSearchParameters = None

    # Stars Archive Wiki Page Writer variables
    __starsArchiveWikiPageWriterSubredditName = None
    __wikiPage = None
    __defaultStarViews = None

    # Initialize the program runner
    def __initializeProgramRunner(self):

        # Setting up logging apparatus
        self.__programRunnerLogger = logging.getLogger('programRunner')

        self.__programRunnerLogger.debug("Initializing the Program Runner")

        # Loading values from configuration file
        # -------------------------------------------------------------------------------

        self.__programRunnerLogger.debug(
            "Retrieving Program Runner initial values from the config. reader"
        )

        configReader = self.__programRunnerIO.getConfigParser()
        try:

            # Scene Info Archiver

            section = 'SceneInfoArchiver'
            sceneInfoArchiverRefreshInterval = configReader.getint(
                section, 'sceneInfoArchiverRefreshInterval'
            )
            sceneInfoArchiverSubredditName = configReader.get(
                section, 'subredditName'
            )
            fromTime = configReader.get(
                section, 'fromTime'
            )
            sceneInfoFlairID = configReader.get(
                section, 'sceneInfoFlairID'
            )
            sceneInfoTextMatcher = re.compile(r'{}'.format(configReader.get(
                section, 'sceneInfoTextMatcherString'
            )))
            movieNameExtractor = re.compile(r'{}'.format(configReader.get(
                section, 'movieNameMatcherString'
            )))
            starsExtractor = re.compile(r'{}'.format(configReader.get(
                section, 'starsMatcherString'
            )))

            # Stars Archive Wiki Page Writer

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

            # Initialization of program instance variables
            # -------------------------------------------------------------------------------
            self.__programRunnerLogger.debug(
                "Setting program initial values"
            )

            # Stars Archive Wiki Page Writer
            self.__programRunnerLogger.debug(
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
                    self.__programRunnerLogger.warning(
                        "'{}' is an invalid Star view and shall"
                        " be removed from the list of provided"
                        " default starviews".format(defaultStarView)
                    )

            # Use default Starviews if list of provided starviews is empty
            if len(validStarViewList) == 0:
                validStarViewList.extend(['individual'])
                self.__programRunnerLogger.warning(
                    "No initial Star views were loaded so the following "
                    "default Star views shall be used for the "
                    "Stars Archive Wiki Page Writer: {}".format(
                        str(validStarViewList)
                    )
                )
            self.__defaultStarViews = validStarViewList

            self.__wikiPage = self.__redditInterface.getPrawReddit() \
                .subreddit(starsArchiveWikiPageWriterSubredditName) \
                .wiki[wikiName]

            # Scene Info Archiver
            self.__programRunnerLogger.debug(
                "Initializing Scene Info Archiver variables"
            )

            self.__sceneInfoArchiverRefreshInterval = sceneInfoArchiverRefreshInterval
            self.__subredditSearchParameters = SubredditSearchParameters(
                sceneInfoArchiverSubredditName,
                fromTime,
                Extractors(
                    sceneInfoFlairID,
                    sceneInfoTextMatcher,
                    movieNameExtractor,
                    starsExtractor
                )
            )

        # Handle if an error occurs while initializing the Program Runner
        except Exception as ex:

            self.__programRunnerLogger.critical(
                "A terminal error occurred while initializing"
                " the Program Runner. Error(s) " + str(ex)
            )
            raise ProgramRunnerInitializationError(ex)

        self.__isProgramRunnerShutdown = False
        self.__programRunnerLogger.info('Program Runner initialized')

    # -------------------------------------------------------------------------------

    # Program Runner commands
    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------

    # Shut down the program runner
    def shutdown(self):
        if not self.__isProgramRunnerShutdown:
            self.__isProgramRunnerShutdown = True
        self.__programRunnerLogger.info(
            "Program Runner successfully shut down"
        )

    # Check if shutdown before running any applications
    def __informIfShutdown(self):
        if self.__isProgramRunnerShutdown:
            self.__programRunnerLogger.warning(
                "The program runner cannot run any more programs "
                "after it has been shut down"
            )
        return self.__isProgramRunnerShutdown

    # -------------------------------------------------------------------------------

    # Program Runner Programs
    # -------------------------------------------------------------------------------
    # -------------------------------------------------------------------------------

    # Scene Info Archiver
    def runSceneInfoArchiver(self):

        # First confirm that the program runner is not shutdown
        if self.__informIfShutdown():
            return

        # Retrieving relevant I/O tools
        programRunnerLogger = self.__programRunnerLogger

        try:

            # Executing the program
            programRunnerLogger.info('Scene Info Archiver is now running')
            nextArchiveOperationTime = datetime.now()

            while True:

                # Quick shutdown check before going forward
                if self.__isProgramRunnerShutdown:
                    programRunnerLogger.info('Scene Info Archiver shut down')
                    break

                # Check if next archiving job is due
                if datetime.now() >= nextArchiveOperationTime:

                    # Storage Archiving task
                    programRunnerLogger.debug(
                        'Scene Info Archiver storage archiving'
                        ' task started'
                    )

                    with self.__programRunnerIO \
                        .getDatabaseConnectionFactory() \
                        .getConnection() \
                            as storageDatabaseConnection:

                        sceneInfoSubmissionsWithSceneInfoStorage = \
                            SceneInfoSubmissionsWithSceneInfoStorage(

                                SceneInfoDAO(
                                    storageDatabaseConnection
                                ),

                                SceneInfoSubmissionDAO(
                                    storageDatabaseConnection
                                ),

                                SceneInfoSubmissionWithSceneInfoDAO(
                                    storageDatabaseConnection
                                )
                            )

                        SceneInfoStorageArchiver.executeSceneInfoArchiver(
                            self.__redditInterface.getPushShiftAPI(),
                            self.__subredditSearchParameters,
                            sceneInfoSubmissionsWithSceneInfoStorage
                        )

                    # Task 1 completo
                    programRunnerLogger.debug(
                        'Scene Info Archiver storage archiving '
                        'task completed'
                    )

                    # Wiki Archiving
                    programRunnerLogger.debug(
                        'Scene Info Archiver wiki archiving'
                        ' task started'
                    )
                    with self.__programRunnerIO \
                        .getDatabaseConnectionFactory() \
                        .getConnection() \
                            as wikiWriterDatabaseConnection:

                        starsArchiveWikiPageWriter = \
                            self.__getNewStarsArchiveWikiPageWriter(
                                wikiWriterDatabaseConnection
                            )
                        starsArchiveWikiPageWriter.writeToWiki()

                        # Task 2 completo
                        programRunnerLogger.debug(
                            'Scene Info Archiver wiki archiving'
                            ' task completed'
                        )

                    # Another quick shutdown check after task completo
                    if self.__isProgramRunnerShutdown:
                        programRunnerLogger.info('Scene Info Archiver shut down')
                        break

                    # Check if task is one-off (i.e. if refresh interval < 0)
                    if self.__sceneInfoArchiverRefreshInterval < 0:
                        programRunnerLogger.info('Scene Info Archiver completed')
                        break

                    # Scheduling next archiving task
                    nextArchiveOperationTime = \
                        datetime.now() + timedelta(
                            minutes=self.__sceneInfoArchiverRefreshInterval
                        )
                    programRunnerLogger.info(
                        'Next Scene Info Archiver archiving job due {}'.format(
                            nextArchiveOperationTime.strftime(
                                "%b %d %Y at %H:%M %z"
                            )
                        )
                    )
                time.sleep(1)

        # Handle if an error occurs while running the Scene Info Archiver
        except Exception as er:
            programRunnerLogger.error(
                "A terminal error occurred while running the Scene "
                "Info Archiver: " + str(er.args), exc_info=True
            )

    # Stars Archive Wiki Page Writer
    def runStarsArchiveWikiPageWriter(self, starViews=None):

        # First confirm that the program runner is not shutdown
        if self.__informIfShutdown():
            return

        # Retrieving relevant I/O tools
        programRunnerLogger = \
            self.__programRunnerLogger

        with self.__programRunnerIO \
                .getDatabaseConnectionFactory()\
                .getConnection() \
                as databaseConnection:

            starsArchiveWikiPageWriter = \
                self.__getNewStarsArchiveWikiPageWriter(
                    databaseConnection, self.__defaultStarViews
                )

            # Executing the program
            programRunnerLogger.info(
                'Stars Archive Wiki Page Writer is now running'
            )
            starsArchiveWikiPageWriter.writeToWiki(starViews)
            programRunnerLogger.info(
                'Stars Archive Wiki Page Writer completed'
            )

    # Convenience method to return a new
    # StarsArchiveWikiPageWriter
    def __getNewStarsArchiveWikiPageWriter(
            self,
            databaseConnection,
            starViews=__defaultStarViews
    ):

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
                self.__programRunnerLogger.warning(
                    "'{}' is an invalid starview and shall"
                    " be removed from the list of provided"
                    " default starviews".format(starView)
                )

        # Use default Starviews if list of provided starviews is empty
        if len(starViewObjects) == 0:
            self.__programRunnerLogger.warning(
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
