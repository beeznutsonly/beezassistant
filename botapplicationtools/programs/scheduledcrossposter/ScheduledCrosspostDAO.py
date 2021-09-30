from typing import List

from botapplicationtools.programs.scheduledcrossposter.ScheduledCrosspost \
    import ScheduledCrosspost


class ScheduledCrosspostDAO:

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def getScheduledCrossposts(self) -> List[ScheduledCrosspost]:
        sqlString = 'SELECT url, subreddit, scheduled_time, title ' \
                    'FROM scheduledcrosspost;'

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString)
            results = cursor.fetchall()

            scheduledCrossposts = []
            for record in results:
                scheduledCrossposts.append(
                    ScheduledCrosspost(
                        record[0],
                        record[1],
                        record[2],
                        record[3]
                    )
                )

            return scheduledCrossposts

        finally:
            cursor.close()

    def getScheduledCrosspostsForUrl(
            self, url: str
    ) -> List[ScheduledCrosspost]:

        sqlString = 'SELECT url, subreddit, scheduled_time, title ' \
                    'FROM ScheduledCrosspost ' \
                    'WHERE url = %s;'

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString, (url,))
            results = cursor.fetchall()

            scheduledCrossposts = []
            for record in results:
                scheduledCrossposts.append(
                    ScheduledCrosspost(
                        record[0],
                        record[1],
                        record[2],
                        record[3]
                    )
                )

            return scheduledCrossposts

        finally:
            cursor.close()

    def checkExists(self, url: str) -> bool:

        sqlString = 'SELECT 1 FROM ScheduledCrosspost ' \
                    'WHERE url = %s;'

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString, (url,))
            result = cursor.fetchone()
            return bool(result)
        finally:
            cursor.close()

    def deleteScheduledCrosspost(
            self,
            scheduledCrosspost: ScheduledCrosspost
    ):

        sqlString = "DELETE FROM ScheduledCrosspost " \
                    "WHERE url = % AND subreddit = %s;"

        cursor = self.__connection.cursor()

        try:
            cursor.execute(
                sqlString,
                (
                    scheduledCrosspost.getUrl,
                    scheduledCrosspost.getSubreddit
                )
            )
            self.__connection.commit()
        finally:
            cursor.close()
