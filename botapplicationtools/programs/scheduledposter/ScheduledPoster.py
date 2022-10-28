from typing import Callable

from praw import Reddit

from botapplicationtools.programs.programtools.generaltools.Decorators import consumestransientapierrors
from botapplicationtools.programs.programtools.programnatures.RecurringProgramNature import RecurringProgramNature
from botapplicationtools.programs.scheduledposter.ScheduledPosterStorage import ScheduledPosterStorage


class ScheduledPoster(RecurringProgramNature):
    """
    Program responsible for submitting
    scheduled submissions
    """

    PROGRAM_NAME: str = "Scheduled Poster"

    def __init__(
            self,
            prawReddit: Reddit,
            scheduledPosterStorage: ScheduledPosterStorage,
            stopCondition: Callable[..., bool],
            cooldown: float = 1
    ):
        super().__init__(
            ScheduledPoster.PROGRAM_NAME,
            stopCondition,
            cooldown
        )
        self.__prawReddit = prawReddit
        self.__scheduledPosterStorage = scheduledPosterStorage

    @consumestransientapierrors
    def _runNatureCore(self, *args, **kwargs):

        # Local variable declaration
        scheduledPosterStorage = self.__scheduledPosterStorage

        scheduledSubmissionDAO = scheduledPosterStorage \
            .getScheduledSubmissionDAO

        completedSubmissionDAO = scheduledPosterStorage \
            .getCompletedSubmissionDAO

        dueSubmissions = scheduledSubmissionDAO.getDueSubmissions()

        for dueSubmission in dueSubmissions:

            # Handle if submission has not been processed
            if not completedSubmissionDAO.checkExists(dueSubmission):
                self._programLogger.debug(
                    'Processing due submission "{}" to subreddit '
                    '"{}" due {}'.format(
                        dueSubmission.getTitle,
                        dueSubmission.getSubreddit,
                        dueSubmission.getScheduledTime
                    )
                )
                submission = self.__prawReddit.subreddit(
                    dueSubmission.getSubreddit
                ).submit(
                    title=dueSubmission.getTitle,
                    url=dueSubmission.getUrl,
                    flair_id=dueSubmission.getFlairId
                )
                self._programLogger.debug(
                    'Post "{}" (ID: {}) to subreddit "{}" due {} '
                    'successfully submitted'.format(
                        dueSubmission.getTitle,
                        submission.id,
                        dueSubmission.getSubreddit,
                        dueSubmission.getScheduledTime
                    )
                )
                completedSubmissionDAO.add(dueSubmission)
                self._programLogger.debug(
                    'Completed submission (ID: {}) successfully '
                    'acknowledged'.format(submission.id)
                )

                # Processing auto-reply for the given submission
                if bool(dueSubmission.getCommentBody):
                    reply = submission.reply(dueSubmission.commentBody)
                    self._programLogger.debug(
                        'Auto reply (ID: {}) for post (ID: {}) '
                        'successfully submitted'.format(
                            reply.id,
                            submission.id
                        )
                    )
