# -*- coding: utf-8 -*

"""
Program responsible for archiving scene info submissions
and the relevant scene info to provided storage
"""
from botapplicationtools.programs.programtools.generaltools import ContributionsUtility
from botapplicationtools.programs.programtools.sceneinfotools import SceneInfoSubmissionsUtility


def execute(
    pushShiftAPI,
    subredditSearchParameters,
    sceneInfoSubmissionsWithSceneInfoStorage
):
    """Execute the program"""

    allSubmissions = ContributionsUtility.retrieveSubmissionsFromSubreddit(
            pushShiftAPI,
            subredditSearchParameters.getSubredditName,
            subredditSearchParameters.getFromTime,
            [
                'id',
                'author',
                'link_flair_template_id',
                'title',
                'created_utc'
            ]
    )

    onlineSubmissions = list(filter(
        lambda submission:
        not ContributionsUtility.isRemoved(submission),
        allSubmissions
    ))

    removedSubmissions = list(filter(
        lambda submission:
        ContributionsUtility.isRemoved(submission),
        allSubmissions
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
