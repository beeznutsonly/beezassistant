# -*- coding: utf-8 -*

from psaw import PushshiftAPI

from botapplicationtools.programs.programtools.generaltools import ContributionsUtility
from botapplicationtools.programs.programtools.generaltools.Decorators import consumestransientapierrors
from botapplicationtools.programs.programtools.generaltools.SimpleSubmission import SimpleSubmission
from botapplicationtools.programs.programtools.programnatures.SimpleProgram import SimpleProgram
from botapplicationtools.programs.programtools.sceneinfotools import SceneInfoSubmissionsUtility
from botapplicationtools.programs.sceneinfostoragearchiver.SceneInfoSubmissionsWithSceneInfoStorage import \
    SceneInfoSubmissionsWithSceneInfoStorage
from botapplicationtools.programs.sceneinfostoragearchiver.SubredditSearchParameters import SubredditSearchParameters


class SceneInfoStorageArchiver(SimpleProgram):
    """
    Program responsible for archiving scene info submissions
    and the relevant scene info to provided storage
    """

    __pushShiftAPI: PushshiftAPI
    __subredditSearchParameters: SubredditSearchParameters
    __sceneInfoSubmissionsWithSceneInfoStorage: \
        SceneInfoSubmissionsWithSceneInfoStorage

    def __init__(
        self,
        pushShiftAPI: PushshiftAPI,
        subredditSearchParameters: SubredditSearchParameters,
        sceneInfoSubmissionsWithSceneInfoStorage:
        SceneInfoSubmissionsWithSceneInfoStorage
    ):
        self.__pushShiftAPI = pushShiftAPI
        self.__subredditSearchParameters = subredditSearchParameters
        self.__sceneInfoSubmissionsWithSceneInfoStorage = \
            sceneInfoSubmissionsWithSceneInfoStorage

    @consumestransientapierrors
    def execute(self):

        # Local variable declaration
        subredditSearchParameters = self.__subredditSearchParameters
        sceneInfoSubmissionsWithSceneInfoStorage = \
            self.__sceneInfoSubmissionsWithSceneInfoStorage

        allSubmissions = ContributionsUtility.retrieveSubmissionsFromSubreddit(
                self.__pushShiftAPI,
                self.__subredditSearchParameters.getSubredditName,
                self.__subredditSearchParameters.getFromTime,
                [
                    'id',
                    'author',
                    'link_flair_template_id',
                    'title',
                    'created_utc',
                    'banned_by'
                ]
        )
        onlineSubmissions = list(filter(
            lambda submission:
            not ContributionsUtility.isRemoved(submission),
            allSubmissions
        ))

        removedSubmissions = list(map(
            lambda submission:
            SimpleSubmission.getSimpleSubmissionFromPrawSubmission(
                submission
            ),
            set(allSubmissions) - set(onlineSubmissions)
        ))

        # Retrieve all scene info submissions from a subreddit within given timeframe
        freshSceneInfoSubmissions = SceneInfoSubmissionsUtility \
            .retrieveSceneInfoSubmissions(
                    onlineSubmissions,
                    subredditSearchParameters.getExtractors
                    .getSceneInfoFlairID
            )

        # Extract scene info from scene info submissions and generate
        # a list of SceneInfoSubmissionsWithSceneInfo objects
        freshSubmissionsAndInfo = SceneInfoSubmissionsUtility \
            .retrieveSceneInfoSubmissionsWithSceneInfo(
                    freshSceneInfoSubmissions,

                    subredditSearchParameters.getExtractors
                    .getSceneInfoTextMatcher,

                    subredditSearchParameters.getExtractors
                    .getMovieNameExtractor,

                    subredditSearchParameters.getExtractors
                    .getStarNamesExtractor
            )

        # Store the scene and submission info to storage
        SceneInfoSubmissionsUtility \
            .saveSceneInfoSubmissionsWithSceneInfoToStorage(
                freshSubmissionsAndInfo,

                sceneInfoSubmissionsWithSceneInfoStorage
                .getSceneInfoSubmissionDAO,

                sceneInfoSubmissionsWithSceneInfoStorage
                .getSceneInfoDAO,

                sceneInfoSubmissionsWithSceneInfoStorage
                .getSceneInfoSubmissionWithSceneInfoDAO,

                removedSubmissions
            )
