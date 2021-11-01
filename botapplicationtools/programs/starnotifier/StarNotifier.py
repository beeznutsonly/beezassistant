"""
Program responsible for notifying users
subscribed to star notifications when a
submission containing a relevant star has
been posted
"""

import time
from typing import Callable

from praw.exceptions import APIException
from prawcore.exceptions import RequestException, ServerError

from botapplicationtools.programs.programtools.generaltools import ContributionsUtility
from botapplicationtools.programs.programtools.starnotificationtools.StarNotificationSubscriptionDAO import \
    StarNotificationSubscriptionDAO
from botapplicationtools.programs.starnotifier.RedditTools import RedditTools
from botapplicationtools.programs.starnotifier.SceneInfoTools import SceneInfoTools


def execute(
        redditTools: RedditTools,
        starNotificationSubscriptionDAO: StarNotificationSubscriptionDAO,
        sceneInfoTools: SceneInfoTools,
        stopCondition: Callable
):
    """Execute the program"""

    # Local variable declaration
    commentStream = redditTools.getCommentStream
    prawReddit = redditTools.getPrawReddit
    sceneInfoCommentMatcher = sceneInfoTools.getSceneInfoCommentMatcher
    starMatcher = sceneInfoTools.getStarMatcher
    # TODO: Kind of bugged, this; will have to revisit
    # sceneInfoFlair = sceneInfoTools.getSceneInfoFlair

    # Program loop
    while not stopCondition():
        try:
            for comment in commentStream:

                # Handle pause token
                if comment is None:

                    if stopCondition():
                        break

                    continue

                try:
                    # Handle if the comment is a scene info comment and
                    # it is not removed
                    if sceneInfoCommentMatcher.search(comment.body).group() \
                    and not ContributionsUtility.isRemoved(comment):
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
                                starNotificationSubscriptionDAO
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

        # Handle for issues connecting to the Reddit API
        except (RequestException, ServerError):

            time.sleep(30)
