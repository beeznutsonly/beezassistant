import json
import logging
import re
import time
from datetime import datetime, timedelta
from typing import List

from praw.models import WikiPage
from psaw import PushshiftAPI

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.GenericProgramRunner import GenericProgramRunner
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoDAO import SceneInfoDAO
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmissionDAO import SceneInfoSubmissionDAO
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmissionWithSceneInfoDAO import \
    SceneInfoSubmissionWithSceneInfoDAO
from botapplicationtools.programs.sceneinfoarchiver import SceneInfoArchiver
from botapplicationtools.programs.sceneinfoarchiver.SceneInfoStorageArchiverTools import SceneInfoStorageArchiverTools
from botapplicationtools.programs.sceneinfoarchiver.StarsArchiveWikiPageWriterTools import \
    StarsArchiveWikiPageWriterTools
from botapplicationtools.programs.sceneinfostoragearchiver.Extractors import Extractors
from botapplicationtools.programs.sceneinfostoragearchiver.SceneInfoSubmissionsWithSceneInfoStorage import \
    SceneInfoSubmissionsWithSceneInfoStorage
from botapplicationtools.programs.sceneinfostoragearchiver.SubredditSearchParameters import SubredditSearchParameters
from botapplicationtools.programs.starsarchivewikipagewriter import StarViewFactory


class SceneInfoArchiverRunner(GenericProgramRunner):

    __sceneInfoArchiverLogger: logging.Logger
    __databaseConnectionFactory: DatabaseConnectionFactory
    __refreshInterval: int

    # Scene Info Storage Archiver variables
    __subredditSearchParameters: SubredditSearchParameters
    __pushShiftAPI: PushshiftAPI

    # Stars Archive Wiki Page Writer variables
    __wikiPage: WikiPage
    __defaultStarViews: List[str]

    def __init__(
            self,
            databaseConnectionFactory,
            redditInterface,
            configReader
    ):
        super(SceneInfoArchiverRunner, self).__init__()
        self.__sceneInfoArchiverLogger = logging.getLogger(
            'sceneInfoArchiverLogger'
        )
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__initializeSceneInfoArchiverRunner(redditInterface, configReader)

    def __initializeSceneInfoArchiverRunner(
            self, redditInterface, configReader
    ):

        # Scene Info Archiver

        section = 'SceneInfoArchiver'
        refreshInterval = configReader.getint(
            section, 'refreshInterval'
        )
        subredditName = configReader.get(
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

        # Initializing default starviews
        validStarViewList = []
        for defaultStarView in defaultStarViews:
            if defaultStarView == 'individual':
                validStarViewList.append(
                    defaultStarView
                )

            # If provided default star view is invalid
            else:
                self.__sceneInfoArchiverLogger.warning(
                    "'{}' is an invalid Star view and shall"
                    " be removed from the list of provided"
                    " default starviews".format(defaultStarView)
                )

        # Use default Starviews if list of provided starviews is empty
        if len(validStarViewList) == 0:
            validStarViewList.extend(['individual'])
            self.__sceneInfoArchiverLogger.warning(
                "No initial StarViews were loaded so the following "
                "default StarViews shall be used for the "
                "Stars Archive Wiki Page Writer: {}".format(
                    str(validStarViewList)
                )
            )
        self.__defaultStarViews = validStarViewList

        self.__wikiPage = redditInterface.getPrawReddit() \
            .subreddit(starsArchiveWikiPageWriterSubredditName) \
            .wiki[wikiName]

        # Scene Info Archiver
        self.__sceneInfoArchiverLogger.debug(
            "Initializing Scene Info Archiver variables"
        )

        self.__refreshInterval = refreshInterval
        self.__pushShiftAPI = redditInterface.getPushShiftAPI()
        self.__subredditSearchParameters = SubredditSearchParameters(
            subredditName,
            fromTime,
            Extractors(
                sceneInfoFlairID,
                sceneInfoTextMatcher,
                movieNameExtractor,
                starsExtractor
            )
        )

    def run(self):

        # First confirm that the program runner is not shutdown
        if self.__informIfShutdown():
            return

        programRunnerLogger = self.__sceneInfoArchiverLogger

        try:

            # Executing the program
            programRunnerLogger.info('Scene Info Archiver is now running')
            nextArchiveOperationTime = datetime.now()

            while True:

                # Quick shutdown check before going forward
                if self.isShutDown():
                    programRunnerLogger.info('Scene Info Archiver shut down')
                    break

                # Check if next archiving job is due
                if datetime.now() >= nextArchiveOperationTime:

                    with self.__databaseConnectionFactory.getConnection() as \
                            storageDatabaseConnection:

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

                        sceneInfoStorageArchiverTools = \
                            SceneInfoStorageArchiverTools(
                                self.__pushShiftAPI,
                                self.__subredditSearchParameters,
                                sceneInfoSubmissionsWithSceneInfoStorage
                            )

                        with self.__databaseConnectionFactory.getConnection() as \
                                wikiWriterDatabaseConnection:

                            starViewObjects = StarViewFactory.getStarViews(
                                wikiWriterDatabaseConnection,
                                self.__defaultStarViews
                            )

                            starsArchiveWikiPageWriterTools = \
                                StarsArchiveWikiPageWriterTools(
                                    self.__wikiPage,
                                    starViewObjects
                                )

                            SceneInfoArchiver.execute(
                                sceneInfoStorageArchiverTools,
                                starsArchiveWikiPageWriterTools,
                            )

                    # Another quick shutdown check after task completo
                    if self.isShutDown():
                        programRunnerLogger.info('Scene Info Archiver shut down')
                        break

                    # Check if task is one-off (i.e. if refresh interval < 0)
                    if self.__refreshInterval < 0:
                        programRunnerLogger.info('Scene Info Archiver completed')
                        break

                    # Scheduling next archiving task
                    nextArchiveOperationTime = \
                        datetime.now() + timedelta(
                            minutes=self.__refreshInterval
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

    def __informIfShutdown(self):
        return self.isShutDown()
