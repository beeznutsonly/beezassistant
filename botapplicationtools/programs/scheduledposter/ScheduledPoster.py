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

    def __init__(
            self,
            prawReddit: Reddit,
            scheduledPosterStorage: ScheduledPosterStorage,
            stopCondition: Callable[..., bool],
            cooldown: float = 1
    ):
        super().__init__(stopCondition, cooldown)
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

        scheduledSubmissionAutoReplyDAO = scheduledPosterStorage \
            .getScheduledSubmissionAutoReplyDAO

        dueSubmissions = scheduledSubmissionDAO.getDueSubmissions()

        for dueSubmission in dueSubmissions:

            # Handle if submission has not been processed
            if not completedSubmissionDAO.checkExists(dueSubmission):
                submission = self.__prawReddit.subreddit(
                    dueSubmission.getSubreddit
                ).submit(
                    title=dueSubmission.getTitle,
                    url=dueSubmission.getUrl,
                    flair_id=dueSubmission.getFlairId
                )
                completedSubmissionDAO.add(dueSubmission)

                # Processing auto-replies for the given submission
                scheduledSubmissionAutoReplies = scheduledSubmissionAutoReplyDAO \
                    .getScheduledSubmissionAutoReplies(dueSubmission)

                for scheduledSubmissionAutoReply in scheduledSubmissionAutoReplies:
                    submission.reply(scheduledSubmissionAutoReply)
