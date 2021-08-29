# -*- coding: utf-8 -*-

"""
Program to automatically reply with Star Info to comments
mentioning a star with scene info archived
"""
from datetime import datetime, timedelta
from itertools import groupby


def execute(
        commentStream,
        starInfoReplyerStorage,
        refreshInterval,
        stopCondition
):
    """Execute the program"""

    starInfoReplyerCommentedDAO = starInfoReplyerStorage \
        .getStarInfoReplyerCommentedDAO

    individualStarViewGroups = __refreshStarInfoGroups(
        starInfoReplyerStorage.getIndividualStarViewDAO
    )

    nextRefreshDue = datetime.now() + timedelta(hours=refreshInterval)

    for comment in commentStream:

        if comment is None:
            if stopCondition():
                break
            if datetime.now() >= nextRefreshDue:
                individualStarViewGroups = __refreshStarInfoGroups(
                    starInfoReplyerStorage.getIndividualStarViewDAO
                )
                nextRefreshDue = datetime.now() + timedelta(
                    hours=refreshInterval
                )
            continue

        if starInfoReplyerCommentedDAO.checkExists(comment.id):
            continue

        for star, records in individualStarViewGroups:
            if star.lower() in comment.body.lower():
                __replyWithStarInfo(comment, star, records)
                starInfoReplyerCommentedDAO.acknowledgeComment(
                    comment.id
                )


def __refreshStarInfoGroups(individualStarViewDAO):
    """
    Update the star info groups with fresh information
    from storage
    """

    individualStarViewRecords = individualStarViewDAO \
        .getIndividualStarViewRecords()
    sortedIndividualStarViewRecords = sorted(
        individualStarViewRecords,
        key=lambda record: record.getStar
    )

    return groupby(
        sortedIndividualStarViewRecords,
        key=lambda record: record.getStar
    )


def __replyWithStarInfo(comment, star, records, limit=None):
    """Reply to the comment with relevant star info"""

    recordsIncluded = []
    if limit:
        recordCount = len(records) if len(records) < limit else limit
    else:
        recordCount = len(records)

    for index in range(0, recordCount - 1):
        if records[index].getSubmissionId == comment.submission.id:
            continue
        recordsIncluded.append(records[index])

    recordCount = len(recordsIncluded)

    if recordCount > 0:
        if recordCount == 1:
            header = '**{}**? We have one other post ' \
                     'of theirs here if you would like to ' \
                     'check it out:\n\n'.format(star)
        else:
            header = '**{}**? We have {} other posts ' \
                     'of theirs here if you would like to ' \
                     'check them out:\n\n'.format(
                        star,
                        str(recordCount) if not limit or (
                                recordCount < limit
                        ) else 'at least ' + str(recordCount)
                     )

        mainBody = ''

        for record in recordsIncluded:
            mainBody += '- [{}]({})\n'.format(
                record.getTitle,
                'https://www.reddit.com/comments/' +
                record.getSubmissionId
            )

        replyMarkDown = header + mainBody

        comment.reply(replyMarkDown)
