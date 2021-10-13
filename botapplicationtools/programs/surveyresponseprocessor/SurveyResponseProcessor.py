import time
from datetime import datetime, timedelta

from praw.exceptions import APIException

from botapplicationtools.programs.programtools.featuretestertools.FeatureTester import FeatureTester
from botapplicationtools.programs.programtools.featuretestertools.FeatureTesterDAO import FeatureTesterDAO
from botapplicationtools.programs.surveyresponseprocessor.RedditTools import RedditTools
from botapplicationtools.programs.surveyresponseprocessor.UserMessage import UserMessage


def execute(
        redditTools: RedditTools,
        featureTesterDAO: FeatureTesterDAO,
        userMessage: UserMessage,
        testingWindow: int
):
    prawReddit = redditTools.getPrawReddit
    subreddit = redditTools.getSubreddit
    userFlairId = redditTools.getUserFlairId

    unprocessedSurveyParticipants = featureTesterDAO.getUnacknowledged()

    for unprocessedSurveyParticipant in unprocessedSurveyParticipants:
        subreddit.flair.set(
            unprocessedSurveyParticipant,
            flair_template_id=userFlairId
        )
        timeIncrementBase = 120
        while True:
            try:
                prawReddit.redditor(unprocessedSurveyParticipant).message(
                    userMessage.getSubject,
                    'Hey {}.\n\n{}'.format(
                        unprocessedSurveyParticipant,
                        userMessage.getBody
                    )
                )
                break
            except APIException as err:
                if err.error_type == "NOT_WHITELISTED_BY_USER_MESSAGE":
                    break
                elif err.error_type == "RATELIMIT":
                    time.sleep(timeIncrementBase + 10)

        featureTesterDAO.acknowledge(
            FeatureTester(
                unprocessedSurveyParticipant,
                datetime.now() + timedelta(
                    days=testingWindow
                )
            )
        )
        time.sleep(20)
