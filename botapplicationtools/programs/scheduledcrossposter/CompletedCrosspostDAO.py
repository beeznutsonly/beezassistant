from botapplicationtools.programs.scheduledcrossposter.ScheduledCrosspost import ScheduledCrosspost


class CompletedCrosspostDAO:

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def add(self, completedCrosspost: ScheduledCrosspost):

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
