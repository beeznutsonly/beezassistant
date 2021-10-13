import time
from typing import Callable

from prawcore.exceptions import RequestException, ServerError

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
    commentStream = redditTools.getCommentStream
    prawReddit = redditTools.getPrawReddit
    sceneInfoCommentMatcher = sceneInfoTools.getSceneInfoCommentMatcher
    starMatcher = sceneInfoTools.getStarMatcher
    sceneInfoFlair = sceneInfoTools.getSceneInfoFlair

    while not stopCondition():
        try:
            for comment in commentStream:

                if comment is None:

                    if stopCondition():
                        break

                    continue

                try:
                    if sceneInfoCommentMatcher.search(
                        comment.body
                    ).group() \
                        and \
                        comment \
                            .submission \
                            .link_flair_template_id == \
                            sceneInfoFlair:

                        stars = starMatcher.findall(
                            comment.body
                        )

                        starNotifications = []
                        for star in stars:
                            starNotifications.extend(
                                starNotificationSubscriptionDAO
                                .getStarNotificationSubscriptionsForStar(
                                    star
                                )
                            )

                        for starNotification in starNotifications:
                            prawReddit.redditor(
                                starNotification.getUsername
                            ).message(
                                "New {} scene available at r/{}"
                                .format(
                                    starNotification.getStar,
                                    comment.subreddit.display_name
                                ),
                                "Hey {}. A new clip featuring {} "
                                "was just posted on r/{}.\n\n"
                                "- [{}]({})".format(
                                    starNotification.getUsername,
                                    starNotification.getStar,
                                    comment.subreddit.display_name,
                                    comment.submission.title,
                                    comment.submission.permalink
                                )
                            )
                except AttributeError:
                    pass

                time.sleep(10)

        except (RequestException, ServerError):

            time.sleep(30)
