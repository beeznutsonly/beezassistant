from praw.models import Message

from botapplicationtools.programs.messagecommandprocessor.commandprocessors.CommandProcessor import CommandProcessor
from botapplicationtools.programs.programtools.sceneinfotools.StarPairSceneInfoSubmissionDetailDAO import \
    StarPairSceneInfoSubmissionDetailDAO


class StarPairPostsCommandProcessor(CommandProcessor):
    """
    Class encapsulating objects responsible for
    processing Star Pair Posts requests
    """

    def __init__(self, connection):
        super().__init__()
        self.__starPairSceneInfoSubmissionDetailDAO = \
            StarPairSceneInfoSubmissionDetailDAO(
                connection
            )

    def processMessage(self, message: Message, *args, **kwargs):

        # Local variable declaration
        messageArguments = message.body
        starNames = messageArguments.split(',', 1)
        response = ''
        unavailableDetails = []

        starPairSceneInfoSubmissionDetails = \
            self.__starPairSceneInfoSubmissionDetailDAO \
                .retrieveSelected(
                    star1=starNames[0].strip(),
                    star2=starNames[1].strip()
                )

        # Handle if star pair is featured in at least one existing post
        if len(starPairSceneInfoSubmissionDetails) > 0:
            response += "Posts featuring **{}** and **{}**:\n\n".format(
                starPairSceneInfoSubmissionDetails[0].getStarNames[0],
                starPairSceneInfoSubmissionDetails[0].getStarNames[1]
            )
            for starPairSceneInfoSubmissionDetail in \
                    starPairSceneInfoSubmissionDetails:

                sceneInfoSubmission = starPairSceneInfoSubmissionDetail \
                    .getSceneInfoSubmission
                response += "- [{}](https://reddit.com/comments/{})\n" \
                    .format(
                        sceneInfoSubmission.getTitle,
                        sceneInfoSubmission.getSubmissionId
                    )
            response += "\n"
        # Handle if there are no existing posts for the provided star
        else:
            unavailableDetails.append((starNames[0], starNames[1]))

        # Handle if there is at least one star without any existing posts
        if len(unavailableDetails) > 0:
            response += "Unfortunately, we do not have posts featuring " \
                        "the following star pairs:\n\n{}".format(
                            "\n".join(
                                list(
                                    map(
                                        lambda unavailableDetail:
                                        "{} and {}".format(
                                            unavailableDetail[0],
                                            unavailableDetail[1]
                                        ),
                                        unavailableDetails
                                    )
                                )
                            )
                        )

        # Responding to the request
        message.reply(response)
        message.mark_read()
