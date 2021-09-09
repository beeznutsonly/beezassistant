# -*- coding: utf-8 -*-

"""
Program to automatically reply with Star Info to comments
mentioning a star with scene info archived
"""

from prawcore import ServerError, RequestException

from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetailDAO \
    import StarSceneInfoSubmissionDetailDAO
import time
from datetime import datetime, timedelta
from itertools import groupby
from typing import List, Callable

from praw import Reddit
from praw.models import Comment

from botapplicationtools.programs.programtools.generaltools import ContributionsUtility
from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetail import \
    StarSceneInfoSubmissionDetail
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerIO import StarInfoReplyerIO


def execute(
        starInfoReplyerIO: StarInfoReplyerIO,
        refreshInterval: int,
        stopCondition: Callable,
        replyFooter: str
):
    """Execute the program"""

    # Program variable initialization

    starInfoReplyerStorage = starInfoReplyerIO.getStarInfoReplyerStorage
    redditTools = starInfoReplyerIO.getRedditTools

    starInfoReplyerCommentedDAO = starInfoReplyerStorage \
        .getStarInfoReplyerCommentedDAO

    starInfoReplyerExcludedDAO = starInfoReplyerStorage \
        .getStarInfoReplyerExcludedDAO

    starInfoGroups = __refreshStarInfoGroups(
        starInfoReplyerStorage
        .getStarSceneInfoSubmissionDetailDAO
    )

    nextGroupsRefreshDue = datetime.now() + timedelta(hours=refreshInterval)

    # Unpacking Reddit tools
    prawReddit = redditTools.getPrawReddit
    commentStream = redditTools.getCommentStream
    excludedUsers = redditTools.getExcludedUsers

    # Program loop
    while not stopCondition():

        try:
            # "Comment listener" loop
            for comment in commentStream:

                # Handle "pause token"
                if comment is None:

                    # Exit the loop if stop condition satisfied 
                    if stopCondition():
                        break
                    
                    # Refresh stored star info groups if due
                    if datetime.now() >= nextGroupsRefreshDue:
                        starInfoGroups = __refreshStarInfoGroups(
                            starInfoReplyerStorage.
                            getStarSceneInfoSubmissionDetailDAO
                        )
                        nextGroupsRefreshDue = datetime.now() + timedelta(
                            hours=refreshInterval
                        )
                    continue

                # Skip processing for removed comments
                if ContributionsUtility.isRemoved(comment):
                    continue
                
                # Skip processing for excluded users
                if (
                        comment.author.name == prawReddit.user.me() or
                        comment.author.name in (
                            [] if excludedUsers is None
                            else excludedUsers
                        ) or
                        starInfoReplyerExcludedDAO.checkExists(
                            comment.author.name
                        )
                ):
                    continue
                
                # Skip processing if comment was previously acknowledged
                if starInfoReplyerCommentedDAO.checkExists(comment.id):
                    continue

                # Iterate through each star for match 
                for star, records in starInfoGroups.items():
                    if star.lower() in comment.body.lower():
                        generatedReply = __replyWithStarInfo(
                            comment, star, records, prawReddit, replyFooter
                        )
                        starInfoReplyerCommentedDAO.acknowledgeComment(
                            comment.id
                        )
                        # Acknowledge bot's generated reply if one is returned
                        if generatedReply:
                            starInfoReplyerCommentedDAO.acknowledgeComment(
                                generatedReply.id
                            )

        # Handle if connection to the Reddit API is lost
        except RequestException or ServerError:
            
            time.sleep(10)


def __refreshStarInfoGroups(
    starSceneInfoSubmissionDetailDAO: 
    StarSceneInfoSubmissionDetailDAO
):
    """
    Update the star info groups with fresh information
    from storage
    """

    starSceneInfoSubmissionDetails = starSceneInfoSubmissionDetailDAO \
        .retrieveAll()

    sortedStarSceneInfoSubmissionDetails = sorted(
        starSceneInfoSubmissionDetails,
        key=lambda record: record.getStarName
    )

    return {
        star: list(records)
        for (star, records) in
        groupby(
            sortedStarSceneInfoSubmissionDetails,
            key=lambda record: record.getStarName
        )
    }


def __replyWithStarInfo(
        comment: Comment,
        star: str,
        records: List[StarSceneInfoSubmissionDetail],
        prawReddit: Reddit,
        footer='',
        limit=5
) -> Comment:
    """
    Replies to the provided comment with relevant 
    star info (if available)
    """

    # Cap the record count according to the limit if 
    # necessary
    if limit:
        recordCount = len(records) if len(records) < limit else limit
    else:
        recordCount = len(records)

    # Process if there are any existing records # TODO: (artifact)
    if recordCount > 0:

        # Header determination

        if recordCount == 1:
            header = '**{}**? We have one post ' \
                     'of theirs here if you would like to ' \
                     'check it out:\n\n'.format(star)
        else:
            header = '**{}**? We have {} posts ' \
                     'of theirs here if you would like to ' \
                     'check them out:\n\n'.format(
                        star,
                        str(recordCount) if (not limit) or (
                                recordCount < limit
                        ) else 'at least ' + str(recordCount)
                     )

        # Main body determination

        mainBody = ''

        sortedRecords = sorted(
            records,
            key=lambda record:
            prawReddit.submission(
                record.getSceneInfoSubmission.getSubmissionId
            ).score,
            reverse=True
        )
        for index in range(0, recordCount):
            sceneInfoSubmission = sortedRecords[index] \
                .getSceneInfoSubmission
            mainBody += '- [{}]({})\n'.format(
                sceneInfoSubmission.getTitle,
                'https://www.reddit.com/comments/' +
                sceneInfoSubmission.getSubmissionId
            )
        mainBody += '\n'

        replyMarkDown = header + mainBody + footer

        return comment.reply(replyMarkDown)
