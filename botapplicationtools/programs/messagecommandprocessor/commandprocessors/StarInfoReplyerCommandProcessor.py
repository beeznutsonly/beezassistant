from botapplicationtools.programs.messagecommandprocessor.commandprocessors.CommandProcessor import CommandProcessor
from botapplicationtools.programs.starinforeplyer.StarInfoReplyerExcludedDAO \
    import StarInfoReplyerExcludedDAO


class StarInfoReplyerCommandProcessor(CommandProcessor):
    """
    Class encapsulating objects responsible for
    processing Star Info Replyer commands
    """

    def __init__(self, connection):
        super().__init__()
        self.__starInfoReplyerExcludedDAO = StarInfoReplyerExcludedDAO(
            connection
        )

    def processMessage(self, message, *args, **kwargs):

        messageArguments = message.body.lower()

        # Process if command is opt-out request
        if messageArguments == "opt-out":

            # Proceed if user had not been previously excluded
            if not self.__starInfoReplyerExcludedDAO.checkExists(
                message.author.name
            ):
                self.__starInfoReplyerExcludedDAO.addUser(
                    message.author.name
                )
                message.reply(
                    "You have been excluded from receiving any "
                    "further Star Info Reply messages. Our "
                    "sincere apologies if the service was an "
                    "inconvenience to you. To opt back into the"
                    " service in the future, [click here]("
                    "https://www.reddit.com/message/compose?"
                    "to=/u/beezassistant&subject=!StarInfoReplyer&"
                    "message=opt-in"
                    ").\n\n Regards.\n\n The r/romanticxxx mod team"
                )

        # Process if command is opt-in request
        elif messageArguments == "opt-in":

            # Proceed if user had been previously excluded
            if self.__starInfoReplyerExcludedDAO.checkExists(
                message.author.name
            ):
                self.__starInfoReplyerExcludedDAO.removeUser(
                    message.author.name
                )
                message.reply(
                    "You have opted into our Star Info Reply "
                    "service. You will now receive updates "
                    "whenever you mention any star we have stored in "
                    "our stars archive. To opt back out, [click here]("
                    "https://www.reddit.com/message/compose?"
                    "to=/u/beezassistant&"
                    "subject=!StarInfoReplyer&"
                    "message=opt-out"
                    ").\n\n Regards.\n\n The r/romanticxxx mod team"
                )

        # Handle unsupported message command arguments
        else:
            message.reply(
                "The bot could not process your message. Please check if "
                "the details you entered in your message are correct, or "
                "contact the r/romanticxxx mods if you're having problems."
                "\n\n Regards.\n\n The r/romanticxxx mod team"
            )
        message.mark_read()
        