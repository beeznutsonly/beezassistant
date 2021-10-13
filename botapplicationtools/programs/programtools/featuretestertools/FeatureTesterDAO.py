from typing import List

from botapplicationtools.programs.programtools.featuretestertools.FeatureTester import FeatureTester


class FeatureTesterDAO:

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def getFeatureTester(self, username: str) -> FeatureTester:
        sqlString = "SELECT username, expiry FROM FeatureTester " \
                    "WHERE username = %s;"

        cursor = self.__connection.cursor()

        try:
            cursor.execute(
                sqlString,
                (username,)
            )
            record = cursor.fetchone()
            if record:
                return FeatureTester(
                    record[0],
                    record[1]
                )
            else:
                return None
        finally:
            cursor.close()

    def getUnacknowledged(self) -> List[str]:

        sqlString = "SELECT username FROM FeatureTester " \
                    "WHERE expiry IS null;"

        cursor = self.__connection.cursor()

        try:
            cursor.execute(
                sqlString
            )
            results = cursor.fetchall()

            unacknowledged = []
            for record in results:
                unacknowledged.append(record[0])

            return unacknowledged

        finally:
            cursor.close()

    def acknowledge(self, featureTester: FeatureTester):

        sqlString = "UPDATE FeatureTester SET expiry = %s " \
                    "WHERE username = %s;"

        cursor = self.__connection.cursor()

        try:
            cursor.execute(
                sqlString,
                (
                    featureTester.getExpiry,
                    featureTester.getUsername
                )
            )
            self.__connection.commit()
        finally:
            cursor.close()
