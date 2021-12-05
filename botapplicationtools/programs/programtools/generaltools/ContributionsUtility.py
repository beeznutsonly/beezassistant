"""
Module providing various utility methods
for submissions and comments
"""
from typing import List, Union

from praw import Reddit
from praw.models import Submission, Comment
from psaw import PushshiftAPI


def retrieveSubmissionsFromSubreddit(
        pushShiftAPI: PushshiftAPI,
        subredditName: str,
        fromTime: str,
        filters: List[str]
) -> List[Submission]:
    """
    Retrieves all submissions from a given subreddit
    after the provided time containing only filtered info
    """

    return list(
        pushShiftAPI.search_submissions(
            subreddit=subredditName,
            after=fromTime,
            filter=filters
        )
    )


def retrieveSelectSubmissions(
        prawReddit: Reddit,
        submissionIds: List[str]
) -> List[Submission]:
    """
    Retrieves submissions with the given
    submissionIds
    """

    submissions = []

    for submissionId in submissionIds:
        submissions.append(
            prawReddit.submission(submissionId)
        )

    return submissions


def isRemoved(
        contribution: Union[Submission, Comment]
) -> bool:
    """
    Checks if provided comment or
    submission is removed
    """

    try:
        author = contribution.author
    except AttributeError:
        author = None
    return author is None or author == '[Deleted]' or \
        contribution.banned_by is not None
