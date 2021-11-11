from botapplicationtools.programs.messagecommandprocessor.commandprocessors.CommandProcessor import CommandProcessor
from botapplicationtools.programs.messagecommandprocessor.messagecommandprocessortools.Decorators import testfeature
from botapplicationtools.programs.programtools.starnotificationtools.StarNotificationSubscription import \
    StarNotificationSubscription
from botapplicationtools.programs.programtools.starnotificationtools.StarNotificationSubscriptionDAO import \
    StarNotificationSubscriptionDAO


class StarNotifierCommandProcessor(CommandProcessor):
    """
    Class encapsulating objects responsible for
    processing Star Notifier requests
    """

    def __init__(self, connection):
        super().__init__()
        self.__starNotificationSubscriptionDAO = StarNotificationSubscriptionDAO(
            connection
        )
        # TODO: Refactor this
        self.__starNotificationLimit = 2

    @testfeature
    def processMessage(self, message, *args, **kwargs):

        # Local variable declaration
        messageArguments = message.body
        userStarNotifications = self.__starNotificationSubscriptionDAO \
            .getUserStarNotificationSubscriptions(message.author.name)

        # Handle if reset subscription request
        if messageArguments == 'reset':
            self.__starNotificationSubscriptionDAO.reset(
                message.author.name
            )
            message.reply(
                "You have successfully reset your notifier preferences. All "
                "your previous subscriptions have been cleared.\n\nRegards."
            )
        # Handle if subscription request
        else:
            # Retrieve stars from message command arguments
            stars = messageArguments.split(',')

            # Check if subscription request does not violate stated quota
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
                # List of user's subscribed stars
                subscribedStarList = list(
                    map(
                        lambda starNotification:
                        starNotification.getUsername.lower(),
                        userStarNotifications
                    )
                )
                for star in stars:
                    # Skip if provided star is already subscribed to
                    if star.strip().lower() in subscribedStarList:
                        continue
                    if len(star.strip()) > 0:
                        # Register star subscription if provided star name
                        # is valid
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

        # Mark read after successful processing
        message.mark_read()
