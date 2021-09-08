from praw.models import Message

from botapplicationtools.programs.starinforeplyer.StarInfoReplyerExcludedDAO \
    import StarInfoReplyerExcludedDAO


class StarInfoReplyerCommandProcessor:
    """
    Class encapsulating objects responsible for
    processing message commands
    """

    __starInfoReplyerExcludedDAO: StarInfoReplyerExcludedDAO

    def __init__(
            self,
            starInfoReplyerExcludedDAO:
            StarInfoReplyerExcludedDAO
    ):
        self.__starInfoReplyerExcludedDAO = starInfoReplyerExcludedDAO

    def processMessage(self, message: Message):

        messageArguments = message.body.lower()

        if messageArguments == "opt-out":
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
        elif messageArguments == "opt-in":
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
                    "to=/u/beezassistant&subject=!StarInfoReplyer&"
                    "message=opt-out"
                    ").\n\n Regards.\n\n The r/romanticxxx mod team"
                )
        else:
            message.reply(
                "The bot could not process your message. Please check if "
                "the details you entered in your message are correct, or "
                "contact the r/romanticxxx mods if you're having problems."
                "\n\n Regards.\n\n The r/romanticxxx mod team"
            )
        message.mark_read()
        