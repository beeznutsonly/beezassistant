from datetime import datetime, timezone
from typing import List

from botapplicationtools.programs.scheduledposter.ScheduledSubmission import ScheduledSubmission


class ScheduledSubmissionDAO:
    """
    DAO class responsible for retrieving
    scheduled submissions
    """

    __connection = None

    def __init__(self, connection):

        self.__connection = connection

    def getDueSubmissions(self) -> List[ScheduledSubmission]:
        """Retrieve all due scheduled submissions"""

        sqlString = "SELECT url, subreddit, title, scheduled_time, flair_id " \
                    "FROM ScheduledSubmission " \
                    "WHERE scheduled_time <= %s;"

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString, (datetime.now(tz=timezone.utc),))
            results = cursor.fetchall()

            dueSubmissions = []
            for record in results:
                dueSubmissions.append(
                    ScheduledSubmission(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        record[4]
                    )
                )
            return dueSubmissions
        finally:
            cursor.close()
