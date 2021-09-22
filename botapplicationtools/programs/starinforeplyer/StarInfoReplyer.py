# -*- coding: utf-8 -*-

"""
Program to automatically reply with Star Info to comments
mentioning a star with scene info archived
"""

import time
from datetime import datetime, timedelta
from itertools import groupby
from typing import Callable, List

from praw import Reddit
from praw.models import Comment
from prawcore.exceptions import RequestException, ServerError

from botapplicationtools.programs.programtools.generaltools import \
    ContributionsUtility
from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetail import \
    StarSceneInfoSubmissionDetail
from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetailDAO import \
    StarSceneInfoSubmissionDetailDAO
from botapplicationtools.programs.starinforeplyer.CustomAddenda import CustomAddenda
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerIO import \
    StarInfoReplyerIO
from botapplicationtools.programs.starinforeplyer.StarStorage import StarStorage


def execute(
        starInfoReplyerIO: StarInfoReplyerIO,
        refreshInterval: int,
        stopCondition: Callable,
        customAddenda: CustomAddenda
):
    """Execute the program"""

    # Program variable initialization

    starInfoReplyerStorage = starInfoReplyerIO.getStarInfoReplyerStorage
    redditTools = starInfoReplyerIO.getRedditTools

    starInfoReplyerCommentedDAO = starInfoReplyerStorage \
        .getStarInfoReplyerCommentedDAO

    starInfoReplyerExcludedDAO = starInfoReplyerStorage \
        .getStarInfoReplyerExcludedDAO

    starStorage = starInfoReplyerStorage.getStarStorage

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
                    
                    # Refresh stored starName info groups if due
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

                # Iterate through each star name for match
                for starName, records in starInfoGroups.items():
                    if starName.lower() in comment.body.lower():
                        generatedReply = __replyWithStarInfo(
                            comment,
                            starName,
                            records,
                            prawReddit,
                            customAddenda,
                            starStorage
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
        except (RequestException, ServerError):
            
            time.sleep(30)


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
        starName: str,
        records: List[StarSceneInfoSubmissionDetail],
        prawReddit: Reddit,
        customAddenda: CustomAddenda,
        starStorage: StarStorage,
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

        mainBody = ''

        # Submission summary determination
        if recordCount == 1:
            submissionSummary = '**{}**? We have one post ' \
                     'of theirs here if you would like to ' \
                     'check it out:\n\n'.format(starName)
        else:
            submissionSummary = '**{}**? We have {} posts ' \
                     'of theirs here if you would like to ' \
                     'check them out:\n\n'.format(
                        starName,
                        str(recordCount) if (not limit) or (
                                recordCount < limit
                        ) else 'at least ' + str(recordCount)
                     )
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
            submissionSummary += '- [{}]({})\n'.format(
                sceneInfoSubmission.getTitle,
                'https://www.reddit.com/comments/' +
                sceneInfoSubmission.getSubmissionId
            )
        mainBody += "{}\n{}\n\n".format(
            submissionSummary,
            customAddenda.getSubmissionSummaryAddendum
        )

        # Star Profile determination
        if starStorage:
            starDAO = starStorage.getStarDAO

            # Proceed if Star Profile exists
            if starDAO.checkExists(starName):
                starProfile = ''
                star = starDAO.getStar(starName)
                starLinks = starStorage.getStarLinkDAO.getStarLinks(star)
                starFirstName = starName.split()[0]

                starProfile += "**More about {}**:\n\n".format(starFirstName)

                starProfile += "- Birthday: {}  \n".format(
                    star.getBirthday.strftime("%d %b %Y")
                ) if star.getBirthday is not None else ""
                starProfile += "- Nationality: {}  \n".format(
                    star.getNationality
                ) if star.getNationality is not None else ""
                starProfile += "- Birth Place: {}  \n".format(
                    star.getBirthPlace
                ) if star.getBirthPlace is not None else ""
                starProfile += "- Nationality: {}  \n".format(
                    star.getNationality
                ) if star.getNationality is not None else ""
                starProfile += "- Years Active: {}  \n".format(
                    star.getYearsActive
                ) if star.getYearsActive is not None else ""

                starProfile += "\n"

                starProfile += "{}\n".format(
                    star.getDescription
                ) if star.getDescription is not None else ""

                # Proceed if star has saved links
                if starLinks:
                    starProfile += "\n"
                    starProfile += "You a fan of **{}**? " \
                                   "Here are a few places you " \
                                   "can support them from:\n\n".format(
                                        starName
                                   )

                    for starLink in starLinks:
                        starProfile += "- [{}]({})\n".format(
                            starLink.getLink if starLink.getLinkName is None
                            else starLink.getLinkName,
                            starLink.getLink
                        )

                mainBody += "{}\n\n".format(starProfile)

        replyMarkDown = mainBody + customAddenda.getFooter

        return comment.reply(replyMarkDown)
