"""
Program responsible for submitting
scheduled submissions
"""

import time

from praw import Reddit
from prawcore.exceptions import RequestException, ServerError

from botapplicationtools.programs.scheduledposter import ScheduledPosterStorage


def execute(
        prawReddit: Reddit,
        scheduledPosterStorage: ScheduledPosterStorage,
        stopCondition
):
    """Execute the program"""

    # Local variable declaration
    scheduledSubmissionDAO = scheduledPosterStorage \
        .getScheduledSubmissionDAO

    completedSubmissionDAO = scheduledPosterStorage \
        .getCompletedSubmissionDAO

    scheduledSubmissionAutoReplyDAO = scheduledPosterStorage \
        .getScheduledSubmissionAutoReplyDAO

    # Program loop
    while not stopCondition():

        dueSubmissions = scheduledSubmissionDAO.getDueSubmissions()

        for dueSubmission in dueSubmissions:
            # Error handling loop
            while True:
                try:
                    # Handle if submission has not been processed
                    if not completedSubmissionDAO.checkExists(dueSubmission):
                        submission = prawReddit.subreddit(
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

                # Handle for problems with the Reddit API
                except (RequestException, ServerError):
                    time.sleep(30)

        # Database check cooldown
        time.sleep(1)
