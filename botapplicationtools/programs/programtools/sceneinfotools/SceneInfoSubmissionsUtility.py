# -*- coding: utf-8 -*

"""
Utility module providing various functions to retrieve,
manipulate, or store scene info and scene info submissions
"""

from botapplicationtools.programs.programtools.sceneinfotools.SceneInfo import SceneInfo
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmissionWithSceneInfo import \
    SceneInfoSubmissionWithSceneInfo


# Retrieve scene info submissions from provided submissions
def retrieveSceneInfoSubmissions(submissions, sceneInfoFlairID):
    sceneInfoSubmissions = []
    for submission in submissions:
        try:
            if str(submission.link_flair_template_id) == sceneInfoFlairID:
                sceneInfoSubmissions.append(submission)
        except AttributeError as ae:
            pass
    return sceneInfoSubmissions


# Retrieve SceneInfoSubmissionWithSceneInfo objects
# from provided scene info submissions
def retrieveSceneInfoSubmissionsWithSceneInfo(
    sceneInfoSubmissions, sceneInfoTextMatcher,
    movieNameExtractor, starNamesExtractor
):
    sceneInfoSubmissionsWithSceneInfo = []
    for sceneInfoSubmission in sceneInfoSubmissions:

        sceneInfoSubmission.comments.replace_more(limit=None)

        # Scanning through all top comments 
        # for relevant scene info
        for topComment in sceneInfoSubmission.comments:

            # Extract the info and stop search once match is found
            if sceneInfoTextMatcher.match(str(topComment.body)):

                movieName = movieNameExtractor.search(str(topComment.body)).group()
                starNames = starNamesExtractor.findall(str(topComment.body))

                sceneInfoSubmissionsWithSceneInfo.append(
                    SceneInfoSubmissionWithSceneInfo(
                        sceneInfoSubmission,
                        SceneInfo(
                            movieName, starNames[0], starNames[1]
                        )
                    )
                )
                break

    return sceneInfoSubmissionsWithSceneInfo


# Save SceneInfoSubmissionsWithSceneInfo data to storage
# through provided DAOs
def saveSceneInfoSubmissionsWithSceneInfoToStorage(
        sceneInfoSubmissionsWithSceneInfo,
        sceneInfoSubmissionDAO,
        sceneInfoDAO,
        sceneInfoSubmissionWithSceneInfoDAO
):

    # Saving submission-specific data
    for sceneInfoSubmissionWithSceneInfo in \
            sceneInfoSubmissionsWithSceneInfo:

        sceneInfoDAO.refreshCursor()
        sceneInfoSubmissionDAO.add(
            sceneInfoSubmissionWithSceneInfo.getSceneInfoSubmission()
        )
    sceneInfoSubmissionDAO.saveChanges()
    sceneInfoSubmissionDAO.closeCursor()

    # Saving scene-specific info
    for sceneInfoSubmissionWithSceneInfo in \
            sceneInfoSubmissionsWithSceneInfo:

        sceneInfoDAO.refreshCursor()
        sceneInfoDAO.add(
            sceneInfoSubmissionWithSceneInfo.getSceneInfo()
        )
    sceneInfoDAO.saveChanges()
    sceneInfoDAO.closeCursor()

    # Saving submission and scene info
    for sceneInfoSubmissionWithSceneInfo in \
            sceneInfoSubmissionsWithSceneInfo:

        sceneInfoDAO.refreshCursor()
        sceneInfoSubmissionWithSceneInfoDAO.add(
            sceneInfoSubmissionWithSceneInfo
        )
    sceneInfoSubmissionWithSceneInfoDAO.saveChanges()
    sceneInfoSubmissionWithSceneInfoDAO.closeCursor()
