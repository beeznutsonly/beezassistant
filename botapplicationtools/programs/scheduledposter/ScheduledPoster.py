import time
from typing import Callable

from praw import Reddit
from prawcore.exceptions import RequestException, ServerError

from botapplicationtools.programs.programtools.programnatures.SimpleProgram import SimpleProgram
from botapplicationtools.programs.scheduledposter.ScheduledPosterStorage import ScheduledPosterStorage


class ScheduledPoster(SimpleProgram):
    """
    Program responsible for submitting
    scheduled submissions
    """

    __prawReddit: Reddit
    __scheduledPosterStorage: ScheduledPosterStorage
    __stopCondition: Callable

    def __init__(
            self,
            prawReddit: Reddit,
            scheduledPosterStorage: ScheduledPosterStorage,
            stopCondition: Callable
    ):
        self.__prawReddit = prawReddit
        self.__scheduledPosterStorage = scheduledPosterStorage
        self.__stopCondition = stopCondition

    def execute(self):

        # Local variable declaration
        scheduledPosterStorage = self.__scheduledPosterStorage

        scheduledSubmissionDAO = scheduledPosterStorage \
            .getScheduledSubmissionDAO

        completedSubmissionDAO = scheduledPosterStorage \
            .getCompletedSubmissionDAO

        scheduledSubmissionAutoReplyDAO = scheduledPosterStorage \
            .getScheduledSubmissionAutoReplyDAO

        # Program loop
        while not self.__stopCondition():

            dueSubmissions = scheduledSubmissionDAO.getDueSubmissions()

            for dueSubmission in dueSubmissions:

                # Error handling loop
                while True:
                    try:
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
                        break

                    # Handle for problems connecting to the Reddit API
                    except (RequestException, ServerError):
                        time.sleep(30)

            # Database check cooldown
            time.sleep(1)
