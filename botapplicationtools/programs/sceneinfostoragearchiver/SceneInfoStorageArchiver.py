# -*- coding: utf-8 -*

"""
Module responsible for archiving scene info submissions
and the relevant scene info to storage
"""

from botapplicationtools.programs.programtools.sceneinfotools import SceneInfoSubmissionsUtility


# Executing the scene info archiver program
def executeSceneInfoArchiver(
    pushShiftAPI,
    subredditSearchParameters,
    sceneInfoSubmissionsWithSceneInfoStorage
):
    # Retrieve all scene info submissions from a subreddit within given timeframe
    freshSceneInfoSubmissions = SceneInfoSubmissionsUtility \
        .retrieveSceneInfoSubmissions(
                __retrieveSubmissions(
                    pushShiftAPI,
                    subredditSearchParameters.getSubredditName(),
                    subredditSearchParameters.getFromTime()
                ),
                subredditSearchParameters.getExtractors()
                    .getSceneInfoFlairID()
        )

    # Extract scene info from scene info submissions and generate
    # a list of SceneInfoSubmissionsWithSceneInfo objects
    freshSubmissionsAndInfo = SceneInfoSubmissionsUtility \
        .retrieveSceneInfoSubmissionsWithSceneInfo(
                freshSceneInfoSubmissions,

                subredditSearchParameters.getExtractors()
                    .getSceneInfoTextMatcher(),

                subredditSearchParameters.getExtractors()
                    .getMovieNameExtractor(),

                subredditSearchParameters.getExtractors()
                    .getStarNamesExtractor()
        )

    # Store the scene and submission info to storage
    SceneInfoSubmissionsUtility \
        .saveSceneInfoSubmissionsWithSceneInfoToStorage(
            freshSubmissionsAndInfo,

            sceneInfoSubmissionsWithSceneInfoStorage
                .getSceneInfoSubmissionDAO(),

            sceneInfoSubmissionsWithSceneInfoStorage
                .getSceneInfoDAO(),

            sceneInfoSubmissionsWithSceneInfoStorage
                .getSceneInfoSubmissionWithSceneInfoDAO()
        )


# Private utility methods
# -------------------------------------------------------------------------------------

# Retrieving all submissions from a given subreddit
# after the provided time
def __retrieveSubmissions(pushShiftAPI, subredditName, fromTime):

    submissions = list(pushShiftAPI.search_submissions(
        subreddit=subredditName,
        after=fromTime,
        filter=['id', 'author', 'link_flair_template_id', 'title', 'created_utc']
    ))

    return list(filter(
        lambda submission: not __is_removed(submission), submissions
    ))


# Checking if a submission is removed
def __is_removed(submission):
    try:
        author = str(submission.author.name)
    except:
        author = '[Deleted]'
    if not (submission.banned_by is None) or author == '[Deleted]':
        return True
    else:
        return False
