from datetime import datetime
from itertools import groupby

from praw.models import Message

from botapplicationtools.programs.programtools.featuretestertools.FeatureTesterDAO import FeatureTesterDAO
from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetailDAO import \
    StarSceneInfoSubmissionDetailDAO


class StarMovieInfoCommandProcessor:
    """
    Class encapsulating objects responsible for
    processing Star Movie Info requests
    """

    __starSceneInfoSubmissionDetailDAO: StarSceneInfoSubmissionDetailDAO
    __featureTesterDAO: FeatureTesterDAO

    def __init__(self, connection):
        self.__starSceneInfoSubmissionDetailDAO = StarSceneInfoSubmissionDetailDAO(
            connection
        )
        self.__featureTesterDAO = FeatureTesterDAO(connection)

    def processMessage(self, message: Message):
        """Process provided message command"""

        # Handle if this is a feature-tester-exclusive feature
        if self.__featureTesterDAO:
            featureTester = self.__featureTesterDAO.getFeatureTester(
                message.author.name
            )
            # Handle if requester is not a feature tester
            if not featureTester:
                message.reply(
                    "Hi {}. Unfortunately, I could not successfully process "
                    "your request because this feature is exclusive to a "
                    "select group of users of which you are not a part of."
                    "\n\nRegards.".format(message.author.name)
                )
                message.mark_read()
                return
            # Handle if feature tester testing window has expired
            if featureTester.getExpiry and featureTester.getExpiry < datetime.now():
                message.reply(
                    "Hi {}. Unfortunately, I could not successfully process "
                    "your request because the time window for using this feature "
                    "on your account expired."
                    "\n\nRegards.".format(message.author.name)
                )
                message.mark_read()
                return

        # Assignment of message arguments (i.e. star in question)
        messageArguments = message.body

        # Retrieving star scene info submission details
        # per the message arguments
        starSceneInfoSubmissionDetails = self.__starSceneInfoSubmissionDetailDAO\
            .retrieveSelected(
                star=messageArguments
            )

        # Variable holding the response body
        response = ''

        # Handle if there exists one or more posts
        # (or scene info submission details) featuring
        # the provided star
        if len(starSceneInfoSubmissionDetails) > 0:

            starName = starSceneInfoSubmissionDetails[0].getStarName

            # Sorting and grouping the scene info submission details
            # by movie name
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

            # Response text build-up
            response += "Movies **{}** is featured in:\n\n---\n\n".format(starName)

            # Processing each movie group
            for movie, records in movieGroups.items():
                response += "**{}**\n\n".format(movie)

                # Processing posts under each movie
                for record in records:
                    response += "- [{}](https://reddit.com/comments/{})\n".format(
                        record.getSceneInfoSubmission.getTitle,
                        record.getSceneInfoSubmission.getSubmissionId
                    )
                    response += "\n"

        # Handle if there exist no posts featuring
        # the provided star
        else:
            response += "Unfortunately, we do not have posts featuring {}.".format(
                messageArguments
            )

        # Responding to the message
        message.reply(response)
        message.mark_read()
