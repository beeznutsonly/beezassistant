import time

from praw import Reddit

from botapplicationtools.programs.scheduledposter import ScheduledPosterStorage


def execute(
        prawReddit: Reddit,
        scheduledPosterStorage: ScheduledPosterStorage,
        stopCondition
):

    scheduledSubmissionDAO = scheduledPosterStorage \
        .getScheduledSubmissionDAO

    completedSubmissionDAO = scheduledPosterStorage \
        .getCompletedSubmissionDAO

    scheduledSubmissionAutoReplyDAO = scheduledPosterStorage \
        .getScheduledSubmissionAutoReplyDAO

    while not stopCondition():

        dueSubmissions = scheduledSubmissionDAO.getDueSubmissions()

        for dueSubmission in dueSubmissions:
            if not completedSubmissionDAO.checkExists(dueSubmission):
                submission = prawReddit.subreddit(
                    dueSubmission.getSubreddit
                ).submit(
                    title=dueSubmission.getTitle,
                    url=dueSubmission.getUrl,
                    flair_id=dueSubmission.getFlairId
                )
                completedSubmissionDAO.add(dueSubmission)

                scheduledSubmissionAutoReplies = scheduledSubmissionAutoReplyDAO \
                    .getScheduledSubmissionAutoReplies(dueSubmission)

                for scheduledSubmissionAutoReply in scheduledSubmissionAutoReplies:
                    submission.reply(scheduledSubmissionAutoReply)

        time.sleep(1)
