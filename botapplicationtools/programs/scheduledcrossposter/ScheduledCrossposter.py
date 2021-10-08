import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from praw.models import Submission
from prawcore.exceptions import RequestException, ServerError

from botapplicationtools.programs.scheduledcrossposter.CompletedCrosspostDAO import CompletedCrosspostDAO
from botapplicationtools.programs.scheduledcrossposter.ScheduledCrosspost import ScheduledCrosspost
from botapplicationtools.programs.scheduledcrossposter.ScheduledCrossposterStorage import ScheduledCrossposterStorage


__LOCK = threading.Lock()


def execute(
        submissionStream,
        scheduledCrossposterStorage: ScheduledCrossposterStorage,
        crosspostProcessor: ThreadPoolExecutor,
        stopCondition
):

    scheduledCrosspostDAO = scheduledCrossposterStorage.getScheduledCrosspostDAO
    completedCrosspostDAO = scheduledCrossposterStorage.getCompletedCrosspostDAO

    while not stopCondition():
        try:
            for submission in submissionStream:

                if submission is None:
                    if stopCondition():
                        break
                    continue

                if scheduledCrosspostDAO.checkExists(
                    submission.url
                ):
                    scheduledCrossposts = scheduledCrosspostDAO \
                        .getScheduledCrosspostsForUrl(
                            submission.url
                        )
                    nonCompletedCrossposts = list(
                        filter(
                            lambda scheduledCrosspost:
                            not completedCrosspostDAO.checkCompleted(
                                scheduledCrosspost
                            ),
                            scheduledCrossposts
                        )
                    )
                    for nonCompletedCrosspost in nonCompletedCrossposts:
                        crosspostProcessor.submit(
                            processNonCompletedCrosspost,
                            nonCompletedCrosspost,
                            submission,
                            completedCrosspostDAO
                        )

        except (RequestException, ServerError):
            time.sleep(30)


def processNonCompletedCrosspost(
        nonCompletedCrosspost: ScheduledCrosspost,
        submission: Submission,
        completedCrosspostDAO: CompletedCrosspostDAO
):

    scheduledTime = nonCompletedCrosspost.getScheduledTime

    while True:
        if datetime.now(tz=timezone.utc) >= scheduledTime:
            submission.crosspost(
                subreddit=nonCompletedCrosspost.getSubreddit,
                title=nonCompletedCrosspost.getTitle
            )
            with __LOCK:
                completedCrosspostDAO.add(nonCompletedCrosspost)
            break

        time.sleep(1)
