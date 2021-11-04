import time
from typing import Callable

from praw.exceptions import APIException
from praw.models import Comment

from botapplicationtools.programs.programtools.generaltools import ContributionsUtility
from botapplicationtools.programs.programtools.programnatures.SimpleStreamProcessorNature import \
    SimpleStreamProcessorNature
from botapplicationtools.programs.programtools.starnotificationtools.StarNotificationSubscriptionDAO import \
    StarNotificationSubscriptionDAO
from botapplicationtools.programs.starnotifier.RedditTools import RedditTools
from botapplicationtools.programs.starnotifier.SceneInfoTools import SceneInfoTools


class StarNotifier(SimpleStreamProcessorNature):
    """
    Program responsible for notifying users
    subscribed to star notifications when a
    submission containing a relevant star has
    been posted
    """

    __redditTools: RedditTools
    __starNotificationSubscriptionDAO: StarNotificationSubscriptionDAO
    __sceneInfoTools: SceneInfoTools

    def __init__(
        self,
        redditTools: RedditTools,
        starNotificationSubscriptionDAO: StarNotificationSubscriptionDAO,
        sceneInfoTools: SceneInfoTools,
        stopCondition: Callable
    ):
        super().__init__(
            redditTools.getCommentStream,
            stopCondition
        )
        self.__redditTools = redditTools
        self.__starNotificationSubscriptionDAO = starNotificationSubscriptionDAO
        self.__sceneInfoTools = sceneInfoTools

    def _runNatureCore(self, comment: Comment):

        # Local variable declaration
        prawReddit = self.__redditTools.getPrawReddit
        sceneInfoCommentMatcher = self.__sceneInfoTools.getSceneInfoCommentMatcher
        starMatcher = self.__sceneInfoTools.getStarMatcher
        # TODO: Kind of bugged, this; will have to revisit
        # sceneInfoFlair = sceneInfoTools.getSceneInfoFlair

        try:
            # Handle if the comment is a scene info comment and
            # it is not removed
            if sceneInfoCommentMatcher.search(comment.body).group() and \
                    not ContributionsUtility.isRemoved(comment):
                # and \
                # comment \
                #     .submission \
                #     .link_flair_template_id == \
                #     sceneInfoFlair:

                stars = starMatcher.findall(
                    comment.body
                )

                starNotifications = []

                # Retrieve all notification subscriptions for
                # each star included in the scene info comment
                for star in stars:
                    starNotifications.extend(
                        self.__starNotificationSubscriptionDAO
                        .getStarNotificationSubscriptionsForStar(
                            star
                        )
                    )

                # Notify all subscribers of the new submission
                for starNotification in starNotifications:
                    while True:
                        try:
                            prawReddit.redditor(
                                starNotification.getUsername
                            ).message(
                                "New {} scene available at r/{}"
                                .format(
                                    starNotification.getStar,
                                    comment.subreddit.display_name
                                ),
                                "Hey {}. A new clip featuring {} "
                                "was just posted to r/{}.\n\n"
                                "- [{}]({})".format(
                                    starNotification.getUsername,
                                    starNotification.getStar,
                                    comment.subreddit.display_name,
                                    comment.submission.title,
                                    comment.submission.permalink
                                )
                            )
                            break

                        # Handle for ratelimit or messaging unavailability
                        # exceptions
                        except APIException as err:
                            if err.error_type == "NOT_WHITELISTED_BY_USER_MESSAGE":
                                break
                            elif err.error_type == "RATELIMIT":
                                time.sleep(120)

        # Handle for non-flaired submissions
        except AttributeError:
            pass
