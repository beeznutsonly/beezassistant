from typing import List

from botapplicationtools.programs.adminupdater.AdminUpdate import AdminUpdate


class AdminUpdateDAO:
    """
    DAO class responsible for
    recording and retrieving admin updates
    to and from storage
    """

    def __init__(self, connection):
        self.__connection = connection

    def retrievePendingAdminUpdates(self) -> List[AdminUpdate]:
        """Retrieve unprocessed admin updates"""

        sqlString = "SELECT id, heading, details FROM AdminUpdate;"
        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString)
            results = cursor.fetchall()
            adminUpdates = []

            for record in results:
                adminUpdates.append(
                    AdminUpdate(
                        record[0],
                        record[1],
                        record[2]
                    )
                )
            return adminUpdates
        finally:
            cursor.close()

    def markCompleted(self, adminUpdates: List[AdminUpdate]):
        """Acknowledge completion of provided admin update"""

        if len(adminUpdates) == 1:
            sqlString = "DELETE FROM AdminUpdate WHERE id = %s;"
        elif len(adminUpdates) > 1:
            sqlString = "DELETE FROM AdminUpdate WHERE id = %s{};".format(
                " OR id = %s" * (len(adminUpdates) - 1)
            )
        else:
            return

        cursor = self.__connection.cursor()
        adminUpdateIds = tuple(map(
            lambda adminUpdate:
            adminUpdate.getId,
            adminUpdates
        ))

        try:
            cursor.execute(
                sqlString,
                adminUpdateIds
            )
            self.__connection.commit()

        finally:
            cursor.close()
