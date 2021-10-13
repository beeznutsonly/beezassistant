from datetime import datetime
from itertools import groupby

from praw.models import Message

from botapplicationtools.programs.programtools.featuretestertools.FeatureTesterDAO import FeatureTesterDAO
from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetailDAO import \
    StarSceneInfoSubmissionDetailDAO


class StarMovieInfoCommandProcessor:

    __starSceneInfoSubmissionDetailDAO: StarSceneInfoSubmissionDetailDAO
    __featureTesterDAO: FeatureTesterDAO

    def __init__(self, connection):
        self.__starSceneInfoSubmissionDetailDAO = StarSceneInfoSubmissionDetailDAO(
            connection
        )
        self.__featureTesterDAO = FeatureTesterDAO(connection)

    def processMessage(self, message: Message):

        if self.__featureTesterDAO:
            featureTester = self.__featureTesterDAO.getFeatureTester(
                message.author.name
            )
            if not featureTester:
                message.reply(
                    "Hi {}. Unfortunately, I could not successfully process "
                    "your request because this feature is exclusive to a "
                    "select group of users of which you are not a part of."
                    "\n\nRegards.".format(message.author.name)
                )
                message.mark_read()
                return
            if featureTester.getExpiry and featureTester.getExpiry < datetime.now():
                message.reply(
                    "Hi {}. Unfortunately, I could not successfully process "
                    "your request because the time window for using this feature "
                    "on your account expired."
                    "\n\nRegards.".format(message.author.name)
                )
                message.mark_read()
                return

        messageArguments = message.body

        starSceneInfoSubmissionDetails = self.__starSceneInfoSubmissionDetailDAO\
            .retrieveSelected(
                star=messageArguments
            )

        response = ''

        if len(starSceneInfoSubmissionDetails) > 0:

            starName = starSceneInfoSubmissionDetails[0].getStarName

            sortedStarSceneInfoSubmissionDetails = sorted(
                starSceneInfoSubmissionDetails,
                key=lambda detail:
                detail.getSceneInfoSubmission.getMovieName
            )
            movieGroups = {
                movie: list(records)
                for (movie, records) in
                groupby(
                    sortedStarSceneInfoSubmissionDetails,
                    key=lambda record:
                    record.getSceneInfoSubmission.getMovieName
                )
            }

            response += "Movies **{}** is featured in:\n\n---\n\n".format(starName)
            for movie, records in movieGroups.items():
                response += "**{}**\n\n".format(movie)

                for record in records:
                    response += "- [{}](https://reddit.com/comments/{})\n".format(
                        record.getSceneInfoSubmission.getTitle,
                        record.getSceneInfoSubmission.getSubmissionId
                    )
                    response += "\n"
        else:
            response += "Unfortunately, we do not have posts featuring {}.".format(
                messageArguments
            )
        message.reply(response)
        message.mark_read()
