from typing import List

from botapplicationtools.programs.scheduledposter.ScheduledSubmission import ScheduledSubmission


class ScheduledSubmissionAutoReplyDAO:
    """
    DAO class responsible for retrieving scheduled
    submission auto-replies
    """

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def getScheduledSubmissionAutoReplies(
            self,
            scheduledSubmission: ScheduledSubmission
    ) -> List[str]:
        """
        Retrieve all auto-replies for the provided
        scheduled submission
        """

        sqlString = 'SELECT comment_body FROM ScheduledSubmissionAutoReply ' \
                    'WHERE url = %s AND subreddit = %s;'
        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString, (
                scheduledSubmission.getUrl,
                scheduledSubmission.getSubreddit
            ))
            results = cursor.fetchall()

            autoReplies = []
            for record in results:
                autoReplies.append(record[0])

            return autoReplies
        finally:
            cursor.close()
