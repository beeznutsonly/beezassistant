import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import ClassVar

from praw.models import Submission
from prawcore.exceptions import RequestException, ServerError

from botapplicationtools.programs.programtools.programnatures.SimpleStreamProcessorNature import \
    SimpleStreamProcessorNature
from botapplicationtools.programs.scheduledcrossposter.ScheduledCrosspost import ScheduledCrosspost
from botapplicationtools.programs.scheduledcrossposter.ScheduledCrossposterStorage import ScheduledCrossposterStorage


class ScheduledCrossposter(SimpleStreamProcessorNature):
    """
    Program responsible for submitting
    Scheduled Crossposts
    """

    # Lock for concurrent write operations
    __LOCK: ClassVar[threading.Lock] = threading.Lock()

    def __init__(
            self,
            submissionStream,
            scheduledCrossposterStorage: ScheduledCrossposterStorage,
            crosspostProcessor: ThreadPoolExecutor,
            stopCondition
    ):
        super().__init__(
            submissionStream,
            stopCondition
        )
        self.__scheduledCrossposterStorage = scheduledCrossposterStorage
        self.__crosspostProcessor = crosspostProcessor

    def _runNatureCore(self, submission):

        scheduledCrossposterStorage = self.__scheduledCrossposterStorage

        # Local variable declaration
        scheduledCrosspostDAO = scheduledCrossposterStorage.getScheduledCrosspostDAO
        completedCrosspostDAO = scheduledCrossposterStorage.getCompletedCrosspostDAO

        # Handle if retrieved submission has
        # scheduled crossposts
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
            # Process each non-completed crosspost
            for nonCompletedCrosspost in nonCompletedCrossposts:
                self.__crosspostProcessor.submit(
                    self.__processNonCompletedCrosspost,
                    nonCompletedCrosspost,
                    submission
                )

    def __processNonCompletedCrosspost(
            self,
            nonCompletedCrosspost: ScheduledCrosspost,
            submission: Submission
    ):
        """
        Process crossposts which have not been
        completed
        """

        scheduledTime = nonCompletedCrosspost.getScheduledTime
        completedCrosspostDAO = self.__scheduledCrossposterStorage \
            .getCompletedCrosspostDAO

        while True:
            try:
                if datetime.now(tz=timezone.utc) >= scheduledTime:
                    submission.crosspost(
                        subreddit=nonCompletedCrosspost.getSubreddit,
                        title=nonCompletedCrosspost.getTitle
                    )
                    with ScheduledCrossposter.__LOCK:
                        completedCrosspostDAO.add(nonCompletedCrosspost)
                    break
                time.sleep(1)

            # Handle if there are problems connecting to the Reddit API
            except(RequestException, ServerError):
                time.sleep(30)
