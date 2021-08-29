# -*- coding: utf-8 -*

"""
Program responsible for archiving scene info submissions
and the relevant scene info to provided storage
"""

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
                __retrieveSubmissions(
                    pushShiftAPI,
                    subredditSearchParameters.getSubredditName,
                    subredditSearchParameters.getFromTime
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


# Private utility methods
# -------------------------------------------------------------------------------------


def __retrieveSubmissions(pushShiftAPI, subredditName, fromTime):
    """
    Retrieving all submissions from a given subreddit
    after the provided time
    """

    submissions = list(pushShiftAPI.search_submissions(
        subreddit=subredditName,
        after=fromTime,
        filter=['id', 'author', 'link_flair_template_id', 'title', 'created_utc']
    ))

    return list(filter(
        lambda submission: not __isRemoved(submission), submissions
    ))


def __isRemoved(submission):
    """Checking if a submission is removed"""

    try:
        author = str(submission.author.name)
    except Exception:
        author = '[Deleted]'
    if not (submission.banned_by is None) or author == '[Deleted]':
        return True
    else:
        return False
