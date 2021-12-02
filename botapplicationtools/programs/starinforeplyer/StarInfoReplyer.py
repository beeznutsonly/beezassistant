# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from itertools import groupby
from typing import Callable, List

from praw.models import Comment

from botapplicationtools.programs.programtools.generaltools import \
    ContributionsUtility
from botapplicationtools.programs.programtools.generaltools.Decorators import consumestransientapierrors
from botapplicationtools.programs.programtools.programnatures.SimpleStreamProcessorNature import \
    SimpleStreamProcessorNature
from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetail import \
    StarSceneInfoSubmissionDetail
from botapplicationtools.programs.starinforeplyer.CustomAddenda import CustomAddenda
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerIO import \
    StarInfoReplyerIO


class StarInfoReplyer(SimpleStreamProcessorNature):
    """
    Program to automatically reply with Star Info to comments
    mentioning a star with scene info archived
    """

    def __init__(
            self,
            starInfoReplyerIO: StarInfoReplyerIO,
            refreshInterval: int,
            stopCondition: Callable,
            customAddenda: CustomAddenda
    ):
        super().__init__(
            starInfoReplyerIO.getRedditTools.getCommentStream,
            stopCondition
        )
        self.__initializeProgram(
            starInfoReplyerIO,
            refreshInterval,
            customAddenda
        )

    def __initializeProgram(
            self,
            starInfoReplyerIO: StarInfoReplyerIO,
            refreshInterval: int,
            customAddenda: CustomAddenda
    ):
        """Initializing the Star Info Replyer"""

        # Program variable initialization

        starInfoReplyerStorage = starInfoReplyerIO.getStarInfoReplyerStorage
        redditTools = starInfoReplyerIO.getRedditTools

        self.__starInfoReplyerCommentedDAO = starInfoReplyerStorage \
            .getStarInfoReplyerCommentedDAO

        self.__starInfoReplyerExcludedDAO = starInfoReplyerStorage \
            .getStarInfoReplyerExcludedDAO

        self.__starSceneInfoSubmissionDetailDAO = starInfoReplyerStorage \
            .getStarSceneInfoSubmissionDetailDAO

        self.__starStorage = starInfoReplyerStorage.getStarStorage
        self.__starInfoGroups = self.__refreshStarInfoGroups()
        self.__refreshInterval = refreshInterval

        self.__nextGroupsRefreshDue = datetime.now() + timedelta(
            hours=refreshInterval
        )

        # Unpacking Reddit tools
        self.__prawReddit = redditTools.getPrawReddit
        self.__excludedUsers = redditTools.getExcludedUsers
        self.__customAddenda = customAddenda

    @consumestransientapierrors
    def _runNatureCore(self, comment: Comment):

        # Skip processing for removed comments
        if ContributionsUtility.isRemoved(comment):
            return

        # Skip processing for excluded users
        if (
                comment.author.name == self.__prawReddit.user.me() or
                comment.author.name in (
                    [] if self.__excludedUsers is None
                    else self.__excludedUsers
                ) or
                self.__starInfoReplyerExcludedDAO.checkExists(
                    comment.author.name
                )
        ):
            return

        # Skip processing if comment was previously acknowledged
        if self.__starInfoReplyerCommentedDAO.checkExists(comment.id):
            return

        # Iterate through each star name for match
        for starName, records in self.__starInfoGroups.items():
            if starName.lower() in comment.body.lower():
                generatedReply = self.__replyWithStarInfo(
                    comment,
                    starName,
                    records
                )
                self.__starInfoReplyerCommentedDAO.acknowledgeComment(
                    comment.id
                )
                # Acknowledge bot's generated reply if one is returned
                if generatedReply:
                    self.__starInfoReplyerCommentedDAO.acknowledgeComment(
                        generatedReply.id
                    )

    def _runPauseHandler(self, *args):

        # Refresh stored starName info groups if due
        if datetime.now() >= self.__nextGroupsRefreshDue:
            self.__starInfoGroups = self.__refreshStarInfoGroups()
            self.__nextGroupsRefreshDue = datetime.now() + timedelta(
                hours=self.__refreshInterval
            )

    def __refreshStarInfoGroups(self):
        """
        Update the star info groups with fresh information
        from storage
        """

        starSceneInfoSubmissionDetails = self.__starSceneInfoSubmissionDetailDAO \
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
            self,
            comment: Comment,
            starName: str,
            records: List[StarSceneInfoSubmissionDetail],
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
                self.__prawReddit.submission(
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
                self.__customAddenda.getSubmissionSummaryAddendum
            )

            # Star Profile determination
            if self.__starStorage:
                starDAO = self.__starStorage.getStarDAO

                # Proceed if Star Profile exists
                if starDAO.checkExists(starName):
                    starProfile = ''
                    star = starDAO.getStar(starName)
                    starLinks = self.__starStorage.getStarLinkDAO.getStarLinks(star)
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

            replyMarkDown = mainBody + self.__customAddenda.getFooter

            return comment.reply(replyMarkDown)
