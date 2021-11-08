from typing import List

from botapplicationtools.programs.programtools.starnotificationtools.StarNotificationSubscription import \
    StarNotificationSubscription


class StarNotificationSubscriptionDAO:

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def add(self, starNotificationSubscription: StarNotificationSubscription):

        sqlString = 'INSERT INTO starnotificationsubscription(username, star) ' \
                    'VALUES (%s, %s);'

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString, (
                starNotificationSubscription.getUsername,
                starNotificationSubscription.getStar
            ))
            self.__connection.commit()
        finally:
            cursor.close()

    def reset(self, username: str):
        sqlString = 'DELETE FROM starnotificationsubscription ' \
                    'WHERE username = %s;'

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString, (username,))
            self.__connection.commit()

        finally:
            cursor.close()

    def getStarNotificationSubscriptionsForStar(self, star: str) -> List[
        StarNotificationSubscription
    ]:

        sqlString = 'SELECT username, star FROM starnotificationsubscription ' \
                    'WHERE star = %s;'

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString, (star,))
            results = cursor.fetchall()

            starNotificationSubscriptions = []
            for record in results:
                starNotificationSubscriptions.append(
                    StarNotificationSubscription(
                        record[0],
                        record[1]
                    )
                )
            return starNotificationSubscriptions

        finally:
            cursor.close()

    def getUserStarNotificationSubscriptions(self, username: str) -> List[
        StarNotificationSubscription
    ]:

        sqlString = 'SELECT username, star FROM StarNotificationSubscription ' \
                    'WHERE username = %s;'

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString, (username,))
            results = cursor.fetchall()

            starNotificationSubscriptions = []
            for record in results:
                starNotificationSubscriptions.append(
                    StarNotificationSubscription(
                        record[0],
                        record[1]
                    )
                )

            return starNotificationSubscriptions
        finally:
            cursor.close()


