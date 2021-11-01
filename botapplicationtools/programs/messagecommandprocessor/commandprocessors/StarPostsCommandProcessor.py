from praw.models import Message

from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetailDAO import \
    StarSceneInfoSubmissionDetailDAO


class StarPostsCommandProcessor:
    """
    Class encapsulating objects responsible for
    processing Star Posts requests
    """

    __starSceneInfoSubmissionDetailDAO: StarSceneInfoSubmissionDetailDAO

    def __init__(self, connection):

        self.__starSceneInfoSubmissionDetailDAO = StarSceneInfoSubmissionDetailDAO(
            connection
        )

    def processMessage(self, message: Message):
        """Process message command"""

        # Local variable declaration
        messageArguments = message.body
        starNames = messageArguments.split(',')
        response = ''
        unavailableDetails = []

        # Handle if provided star arguments exceed maximum threshold
        if len(starNames) > 10:  # TODO: De-hardcode threshold
            message.reply(
                "You have provided too many arguments. "
                "We only allow a maximum of 10 stars per "
                "request."
            )
            message.mark_read()
            return

        # Processing each provided star argument
        for starName in starNames:
            starSceneInfoSubmissionDetails = self.__starSceneInfoSubmissionDetailDAO \
                .retrieveSelected(
                    star=starName.strip()
                )
            # Handle if star is featured in at least one existing post
            if len(starSceneInfoSubmissionDetails) > 0:
                response += "Posts featuring **{}**:\n\n".format(
                    starSceneInfoSubmissionDetails[0].getStarName
                )
                for starSceneInfoSubmissionDetail in starSceneInfoSubmissionDetails:
                    sceneInfoSubmission = starSceneInfoSubmissionDetail \
                        .getSceneInfoSubmission
                    response += "- [{}](https://reddit.com/comments/{})\n" \
                        .format(
                            sceneInfoSubmission.getTitle,
                            sceneInfoSubmission.getSubmissionId
                        )
                response += "\n"
            # Handle if there are no existing posts for the provided star
            else:
                unavailableDetails.append(starName)

            # Handle if there is at least one star without any existing posts
            if len(unavailableDetails) > 0:
                response += "Unfortunately, we do not have posts featuring " \
                            "the following stars: {}".format(
                                ", ".join(unavailableDetails)
                            )

        # Responding to the request
        message.reply(response)
        message.mark_read()
