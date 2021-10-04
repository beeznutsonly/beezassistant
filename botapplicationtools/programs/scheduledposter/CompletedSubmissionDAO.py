from botapplicationtools.programs.scheduledposter.ScheduledSubmission import ScheduledSubmission


class CompletedSubmissionDAO:

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def add(self, dueSubmission: ScheduledSubmission):

        sqlString = 'INSERT INTO CompletedSubmission (url, subreddit) ' \
                    'VALUES (%s, %s);'
        cursor = self.__connection.cursor()

        try:
            cursor.execute(
                sqlString,
                (
                    dueSubmission.getUrl,
                    dueSubmission.getSubreddit
                )
            )
            self.__connection.commit()
        finally:
            cursor.close()

    def checkExists(self, scheduledSubmission: ScheduledSubmission):

        sqlString = 'SELECT 1 FROM CompletedSubmission WHERE ' \
                    'url = %s AND subreddit = %s;'
        cursor = self.__connection.cursor()

        try:
            cursor.execute(
                sqlString,
                (
                    scheduledSubmission.getUrl,
                    scheduledSubmission.getSubreddit
                )
            )
            result = cursor.fetchone()
            return bool(result)
        finally:
            cursor.close()
