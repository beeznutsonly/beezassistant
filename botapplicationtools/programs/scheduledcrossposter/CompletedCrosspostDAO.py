from botapplicationtools.programs.scheduledcrossposter.ScheduledCrosspost import ScheduledCrosspost


class CompletedCrosspostDAO:
    """
    DAO class responsible for marking and
    checking completed crossposts to and
    from storage respectively
    """

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def add(self, completedCrosspost: ScheduledCrosspost):
        """Add (Mark) completed crosspost"""

        sqlString = 'INSERT INTO CompletedCrosspost(url, subreddit) VALUES ' \
                    '(%s, %s);'

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString, (
                completedCrosspost.getUrl,
                completedCrosspost.getSubreddit
            ))
            self.__connection.commit()
        finally:
            cursor.close()

    def checkCompleted(self, scheduledCrosspost: ScheduledCrosspost) -> bool:
        """Check if provided scheduled crosspost has been completed"""

        sqlString = 'SELECT 1 FROM CompletedCrosspost ' \
                    'WHERE url=%s AND subreddit=%s;'

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString, (
                scheduledCrosspost.getUrl,
                scheduledCrosspost.getSubreddit
            ))
            result = cursor.fetchone()
            return bool(result)
        finally:
            cursor.close()
