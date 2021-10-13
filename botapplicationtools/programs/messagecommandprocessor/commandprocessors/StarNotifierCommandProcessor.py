from datetime import datetime

from praw.models import Message

from botapplicationtools.programs.programtools.featuretestertools.FeatureTesterDAO import FeatureTesterDAO
from botapplicationtools.programs.programtools.starnotificationtools.StarNotificationSubscription import \
    StarNotificationSubscription
from botapplicationtools.programs.programtools.starnotificationtools.StarNotificationSubscriptionDAO import \
    StarNotificationSubscriptionDAO


class StarNotifierCommandProcessor:
    """"""

    __starNotificationSubscriptionDAO = None
    __featureTesterDAO = None
    __starNotificationLimit: int

    def __init__(
            self,
            connection
    ):
        """"""
        self.__starNotificationSubscriptionDAO = StarNotificationSubscriptionDAO(
            connection
        )
        self.__featureTesterDAO = FeatureTesterDAO(connection)
        # TODO: Refactor this
        self.__starNotificationLimit = 2

    def processMessage(self, message: Message):

        messageArguments = message.body
        stars = messageArguments.split(',')
        userStarNotifications = self.__starNotificationSubscriptionDAO \
            .getUserStarNotificationSubscriptions(message.author.name)

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

        if messageArguments == 'reset':
            self.__starNotificationSubscriptionDAO.reset(
                message.author.name
            )
            message.reply(
                "You have successfully reset your notifier preferences. All "
                "your previous subscriptions have been cleared.\n\nRegards."
            )
        else:
            if (len(userStarNotifications) + len(stars)) > \
                    self.__starNotificationLimit:
                message.reply(
                    "Hi {}. Unfortunately, I could not successfully process your "
                    "request because it goes beyond your allocated quota of "
                    "notification subscriptions ({}). Please try again, but "
                    "within the specified limit or click [here]"
                    "(https://www.reddit.com/message/compose?"
                    "to=/u/beezassistant&subject=!StarNotifier&"
                    "message=reset) to reset your previous subscriptions.".format(
                        message.author.name,
                        self.__starNotificationLimit
                    )
                )
            else:
                subscribedStarList = list(
                    map(
                        lambda starNotification:
                        starNotification.getUsername.lower(),
                        userStarNotifications
                    )
                )
                for star in stars:
                    if star.strip().lower() in subscribedStarList:
                        continue
                    if len(star.strip()) > 0:
                        self.__starNotificationSubscriptionDAO.add(
                            StarNotificationSubscription(
                                message.author.name,
                                star.strip()
                            )
                        )
                message.reply(
                    "You have successfully subscribed to notifications "
                    "for the following stars:\n\n- {}\n\nYou may reset "
                    "your subscriptions by following this [link]"
                    "(https://www.reddit.com/message/compose?"
                    "to=/u/beezassistant&subject=!StarNotifier&"
                    "message=reset).\n\nRegards.".format(
                        '\n- '.join(stars)
                    )
                )
        message.mark_read()
