from typing import List


class StarInfoReplyerExcludedDAO:
    """
    DAO class responsible for checking for and
    adding users excluded from the
    Star Info Replyer service
    """

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def addUser(self, username: str):
        """Add excluded user"""

        sqlString = "INSERT INTO StarInfoReplyerExcluded(username)" \
                    " VALUES (%s) ON CONFLICT DO NOTHING;"

        cursor = self.__connection.cursor()
        try:
            cursor.execute(sqlString, (username,))
            self.__connection.commit()
        except Exception as ex:
            raise ex
        finally:
            cursor.close()

    def removeUser(self, username: str):
        """Remove excluded user"""

        sqlString = "DELETE FROM StarInfoReplyerExcluded " \
                    "WHERE username = %s;"

        cursor = self.__connection.cursor()
        try:
            cursor.execute(sqlString, (username,))
            self.__connection.commit()
        except Exception as ex:
            raise ex
        finally:
            cursor.close()

    def retrieve(self) -> List[str]:
        """Retrieve a list of all excluded users"""

        sqlString = "SELECT username FROM StarInfoReplyerExcluded"

        cursor = self.__connection.cursor()
        try:
            cursor.execute(sqlString)
            results = cursor.fetchall()
            excludedUsers = []
            for record in results:
                excludedUsers.append(record[0])
            return excludedUsers
        except Exception as ex:
            raise ex
        finally:
            cursor.close()

    def checkExists(self, username: str) -> bool:
        """
        Check if provided username exists in
        storage
        """

        sqlString = 'SELECT username FROM ' \
                    'StarInfoReplyerExcluded ' \
                    'WHERE username=%s;'

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString, (username,))
            return bool(cursor.fetchone())
        except Exception as ex:
            raise ex
        finally:
            cursor.close()
