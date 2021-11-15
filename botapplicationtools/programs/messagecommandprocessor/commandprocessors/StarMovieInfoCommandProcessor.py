from itertools import groupby

from botapplicationtools.programs.messagecommandprocessor.commandprocessors.CommandProcessor import CommandProcessor
from botapplicationtools.programs.messagecommandprocessor.messagecommandprocessortools.Decorators import testfeature
from botapplicationtools.programs.messagecommandprocessor.messagecommandprocessortools.testfeaturetools.FeatureTesterDAO import FeatureTesterDAO
from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetailDAO import \
    StarSceneInfoSubmissionDetailDAO


class StarMovieInfoCommandProcessor(CommandProcessor):
    """
    Class encapsulating objects responsible for
    processing Star Movie Info requests
    """

    def __init__(self, connection):
        super().__init__()
        self.__starSceneInfoSubmissionDetailDAO = StarSceneInfoSubmissionDetailDAO(
            connection
        )
        self.__featureTesterDAO = FeatureTesterDAO(connection)

    @testfeature
    def processMessage(self, message, *args, **kwargs):

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
