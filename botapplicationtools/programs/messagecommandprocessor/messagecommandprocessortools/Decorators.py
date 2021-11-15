import functools
from datetime import datetime

from praw.models import Message


def testfeature(processMessageFunction):
    """
    Decorator responsible for handling requests for
    test features from users
    """

    @functools.wraps(processMessageFunction)
    def wrapper(
            self,
            message: Message,
            *args,
            **kwargs
    ):

        # Local variable initialization
        featureTesterDAO = kwargs["featureTesterDAO"]
        featureTester = featureTesterDAO.getFeatureTester(
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

        processMessageFunction(self, message, featureTesterDAO, *args, **kwargs)

    return wrapper
