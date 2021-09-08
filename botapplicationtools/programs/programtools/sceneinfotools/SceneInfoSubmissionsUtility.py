# -*- coding: utf-8 -*

"""
Utility module providing various functions to retrieve,
manipulate, or store scene info and scene info submissions
"""
from botapplicationtools.programs.programtools.generaltools.SimpleSubmission import SimpleSubmission
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmission import SceneInfoSubmission
import re
from typing import List

from praw.models import Submission

from botapplicationtools.programs.programtools.sceneinfotools.SimpleSceneInfo \
    import SimpleSceneInfo
from botapplicationtools.programs.programtools.sceneinfotools.SimpleSceneInfoDAO \
    import SimpleSceneInfoDAO
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmissionDAO \
    import SceneInfoSubmissionDAO
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmissionWithSceneInfo \
    import SceneInfoSubmissionWithSceneInfo
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmissionWithSceneInfoDAO \
    import SceneInfoSubmissionWithSceneInfoDAO


def retrieveSceneInfoSubmissions(
        submissions: List[Submission],
        sceneInfoFlairID: str
):
    """Retrieve scene info submissions from provided submissions"""

    sceneInfoSubmissions = []
    for submission in submissions:
        try:
            if str(submission.link_flair_template_id) == sceneInfoFlairID:
                sceneInfoSubmissions.append(submission)
        except AttributeError:
            pass
    return sceneInfoSubmissions


def retrieveSceneInfoSubmissionsWithSceneInfo(
    sceneInfoSubmissions: List[Submission],
    sceneInfoTextMatcher: re.Pattern,
    movieNameExtractor: re.Pattern,
    starNamesExtractor: re.Pattern
) -> List[SceneInfoSubmissionWithSceneInfo]:
    """
    Retrieve SceneInfoSubmissionWithSceneInfo objects
    from provided scene info submissions
    """

    sceneInfoSubmissionsWithSceneInfo = []
    for sceneInfoSubmission in sceneInfoSubmissions:

        sceneInfoSubmission.comments.replace_more(limit=None)

        # Scanning through all top comments 
        # for relevant scene info
        for topComment in sceneInfoSubmission.comments:

            # Extract the info and stop search once match is found
            if sceneInfoTextMatcher.match(topComment.body):

                movieName = movieNameExtractor.search(topComment.body).group()
                starNames = starNamesExtractor.findall(topComment.body)

                sceneInfoSubmissionsWithSceneInfo.append(
                    SceneInfoSubmissionWithSceneInfo(
                        
                        SceneInfoSubmission
                        .getSceneInfoSubmissionFromPrawSubmission(
                            sceneInfoSubmission
                        ),

                        SimpleSceneInfo(
                            movieName, starNames[0], starNames[1]
                        )
                    )
                )
                break

    return sceneInfoSubmissionsWithSceneInfo


def saveSceneInfoSubmissionsWithSceneInfoToStorage(
        sceneInfoSubmissionsWithSceneInfo:
        SceneInfoSubmissionWithSceneInfo,

        sceneInfoSubmissionDAO:
        SceneInfoSubmissionDAO,

        sceneInfoDAO:
        SimpleSceneInfoDAO,

        sceneInfoSubmissionWithSceneInfoDAO:
        SceneInfoSubmissionWithSceneInfoDAO,

        removedSubmissions:
        List[SimpleSubmission] = None,
):
    """
    Save SceneInfoSubmissionsWithSceneInfo data to storage
    through provided DAOs
    """

    # Saving submission-specific data
    sceneInfoSubmissionDAO.refreshCursor()
    for sceneInfoSubmissionWithSceneInfo in \
            sceneInfoSubmissionsWithSceneInfo:

        sceneInfoSubmissionDAO.add(
            sceneInfoSubmissionWithSceneInfo.getSceneInfoSubmission
        )
    # Optionally remove removed submissions
    if removedSubmissions:
        for removedSubmission in removedSubmissions:
            sceneInfoSubmissionDAO.remove(removedSubmission)
    sceneInfoSubmissionDAO.saveChanges()
    sceneInfoSubmissionDAO.closeCursor()

    # Saving scene-specific info
    sceneInfoDAO.refreshCursor()
    for sceneInfoSubmissionWithSceneInfo in \
            sceneInfoSubmissionsWithSceneInfo:

        sceneInfoDAO.add(
            sceneInfoSubmissionWithSceneInfo.getSceneInfo
        )
    sceneInfoDAO.saveChanges()
    sceneInfoDAO.closeCursor()

    # Saving submission and scene info
    sceneInfoSubmissionWithSceneInfoDAO.refreshCursor()
    for sceneInfoSubmissionWithSceneInfo in \
            sceneInfoSubmissionsWithSceneInfo:

        sceneInfoSubmissionWithSceneInfoDAO.add(
            sceneInfoSubmissionWithSceneInfo
        )
    sceneInfoSubmissionWithSceneInfoDAO.saveChanges()
    sceneInfoSubmissionWithSceneInfoDAO.closeCursor()
