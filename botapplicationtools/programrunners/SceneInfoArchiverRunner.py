# -*- coding: utf-8 -*-

import json
import re
import time
from datetime import datetime, timedelta
from typing import List

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.programrunners.ProgramRunner import ProgramRunner
from botapplicationtools.programs.programtools.sceneinfotools.SimpleSceneInfoDAO import SimpleSceneInfoDAO
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
from botapplicationtools.programsexecutors.programsexecutortools.RedditInterfaceFactory import RedditInterfaceFactory


class SceneInfoArchiverRunner(ProgramRunner):
    """
    Class responsible for running multiple
    SceneInfoArchiver program instances
    """

    __refreshInterval: int

    # Scene Info Storage Archiver variables
    __subredditSearchParameters: SubredditSearchParameters

    # Stars Archive Wiki Page Writer variables
    __wikiName: str
    __subredditName: str
    __defaultStarViews: List[str]

    def __init__(
            self,
            redditInterfaceFactory,
            databaseConnectionFactory,
            configReader
    ):
        super().__init__(
            redditInterfaceFactory,
            databaseConnectionFactory,
            "Scene Info Archiver Runner"
        )
        self.__redditInterfaceFactory = redditInterfaceFactory
        self.__databaseConnectionFactory = databaseConnectionFactory
        self.__initializeProgramRunner(configReader)

    def __initializeProgramRunner(
            self, configReader
    ):
        """Initializing the scene info archiver"""

        # Retrieving values from config file
        # -------------------------------------------------------------------------------

        # Scene Info Storage Archiver values

        section = 'SceneInfoArchiverRunner'
        userProfile = configReader.get(
            section, "userProfile"
        )
        refreshInterval = configReader.getint(
            section, 'refreshInterval'
        )
        sceneInfoStorageArchiverSubredditName = configReader.get(
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

        # Stars Archive Wiki Page Writer values

        section = 'StarsArchiveWikiPageWriterRunner'
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

        # General

        self._userProfile = userProfile
        self.__refreshInterval = refreshInterval

        # For Scene Info Storage Archiver

        self.__subredditSearchParameters = SubredditSearchParameters(
            sceneInfoStorageArchiverSubredditName,
            fromTime,
            Extractors(
                sceneInfoFlairID,
                sceneInfoTextMatcher,
                movieNameExtractor,
                starsExtractor
            )
        )

        # For Stars Archive Wiki Page Writer

        self.__subredditName = starsArchiveWikiPageWriterSubredditName
        self.__wikiName = wikiName
        # TODO: Clean up this shoddiness
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
                "No initial StarViews were loaded so the following "
                "default StarViews shall be used for the "
                "Stars Archive Wiki Page Writer: {}".format(
                    str(validStarViewList)
                )
            )
        self.__defaultStarViews = validStarViewList

    def _runCore(self, redditInterface, connection):

        programRunnerLogger = self._programRunnerLogger
        nextArchiveOperationTime = datetime.now()

        while not self.isShutDown():

            # Check if next archiving job is due
            if datetime.now() >= nextArchiveOperationTime:

                sceneInfoSubmissionsWithSceneInfoStorage = \
                    SceneInfoSubmissionsWithSceneInfoStorage(

                        SimpleSceneInfoDAO(
                            connection
                        ),

                        SceneInfoSubmissionDAO(
                            connection
                        ),

                        SceneInfoSubmissionWithSceneInfoDAO(
                            connection
                        )
                    )

                sceneInfoStorageArchiverTools = \
                    SceneInfoStorageArchiverTools(

                        redditInterface.getPushShiftAPI,

                        self.__subredditSearchParameters,

                        sceneInfoSubmissionsWithSceneInfoStorage
                    )

                starViewObjects = StarViewFactory.getStarViews(
                    connection,
                    self.__defaultStarViews
                )

                starsArchiveWikiPageWriterTools = \
                    StarsArchiveWikiPageWriterTools(
                        redditInterface
                        .getPrawReddit
                        .subreddit(self.__subredditName)
                        .wiki[self.__wikiName],

                        starViewObjects
                    )

                SceneInfoArchiver.execute(
                    sceneInfoStorageArchiverTools,
                    starsArchiveWikiPageWriterTools,
                )

                # Check if task is one-off (i.e. if refresh interval < 0)
                if self.__refreshInterval < 0:
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
