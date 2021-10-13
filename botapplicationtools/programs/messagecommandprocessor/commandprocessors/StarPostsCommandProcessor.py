from praw.models import Message

from botapplicationtools.programs.programtools.sceneinfotools.StarSceneInfoSubmissionDetailDAO import \
    StarSceneInfoSubmissionDetailDAO


class StarPostsCommandProcessor:

    __starSceneInfoSubmissionDetailDAO: StarSceneInfoSubmissionDetailDAO

    def __init__(self, connection):

        self.__starSceneInfoSubmissionDetailDAO = StarSceneInfoSubmissionDetailDAO(
            connection
        )

    def processMessage(self, message: Message):

        messageArguments = message.body
        starNames = messageArguments.split(',')
        response = ''
        unavailableDetails = []

        if len(starNames) > 10:
            message.reply(
                "You have provided too many arguments. "
                "We only allow a maximum of 10 stars per "
                "request."
            )
            message.mark_read()
            return

        for starName in starNames:
            starSceneInfoSubmissionDetails = self.__starSceneInfoSubmissionDetailDAO \
                .retrieveSelected(
                    star=starName.strip()
                )
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
            else:
                unavailableDetails.append(starName)

            if len(unavailableDetails) > 0:
                response += "Unfortunately, we do not have posts featuring " \
                            "the following stars: {}".format(
                                ", ".join(unavailableDetails)
                            )

        message.reply(response)
        message.mark_read()

