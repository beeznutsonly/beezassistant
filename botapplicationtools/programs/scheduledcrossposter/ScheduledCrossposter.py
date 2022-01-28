import threading
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import ClassVar

from praw.models import Submission
from prawcore import PrawcoreException

from botapplicationtools.programs.programtools.generaltools.Decorators import consumestransientapierrors
from botapplicationtools.programs.programtools.programnatures.streamprocessingnature.SimpleStreamProcessorNature import \
    SimpleStreamProcessorNature
from botapplicationtools.programs.programtools.programnatures.streamprocessingnature.SimpleSubmissionStreamFactory import \
    SimpleSubmissionStreamFactory
from botapplicationtools.programs.scheduledcrossposter.ScheduledCrosspost import ScheduledCrosspost
from botapplicationtools.programs.scheduledcrossposter.ScheduledCrossposterStorage import ScheduledCrossposterStorage


class ScheduledCrossposter(SimpleStreamProcessorNature):
    """
    Program responsible for submitting
    Scheduled Crossposts
    """

    PROGRAM_NAME: str = "Scheduled Crossposter"

    # Lock for concurrent write operations
    __LOCK: ClassVar[threading.Lock] = threading.Lock()

    def __init__(
            self,
            submissionStreamFactory: SimpleSubmissionStreamFactory,
            scheduledCrossposterStorage: ScheduledCrossposterStorage,
            crosspostProcessor: ThreadPoolExecutor,
            stopCondition
    ):
        super().__init__(
            submissionStreamFactory,
            stopCondition,
            ScheduledCrossposter.PROGRAM_NAME
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

    @consumestransientapierrors
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

        self._programLogger.debug(
            'Processing non-completed crosspost to {}, '
            'for submission "{}" (ID: {}) due {}'.format(
                nonCompletedCrosspost.getSubreddit,
                submission.title,
                submission.id,
                scheduledTime
            )
        )

        while True:
            if datetime.now(tz=timezone.utc) >= scheduledTime:
                try:
                    successfulCrosspost = submission.crosspost(
                        subreddit=nonCompletedCrosspost.getSubreddit,
                        title=nonCompletedCrosspost.getTitle
                    )
                    self._programLogger.debug(
                        'Crosspost "{}" (ID: {}) to {}, for submission "{}" (ID: {}) '
                        'due {} completed'.format(
                            successfulCrosspost.title,
                            successfulCrosspost.id,
                            nonCompletedCrosspost.getSubreddit,
                            submission.title,
                            submission.id,
                            scheduledTime
                        )
                    )
                    with ScheduledCrossposter.__LOCK:
                        completedCrosspostDAO.add(nonCompletedCrosspost)
                        self._programLogger.debug(
                            "Completion of crosspost (ID: {}) successfully "
                            "acknowledged".format(successfulCrosspost.id)
                        )
                    break
                except PrawcoreException as ex:
                    self._programLogger.error(
                        'Non-completed crosspost to {} for submission "{}" '
                        '(ID: {}) due {} failed: ' + str(ex.args)
                    )
            time.sleep(1)
