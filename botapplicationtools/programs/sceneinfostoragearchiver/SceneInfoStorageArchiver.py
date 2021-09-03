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

    # Retrieve all scene info submissions from a subreddit within given timeframe
    freshSceneInfoSubmissions = SceneInfoSubmissionsUtility \
        .retrieveSceneInfoSubmissions(
                ContributionsUtility.retrieveSubmissionsFromSubreddit(
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
                ),
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
            .getSceneInfoSubmissionWithSceneInfoDAO
        )
