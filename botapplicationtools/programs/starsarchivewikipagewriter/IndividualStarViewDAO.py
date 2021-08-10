# -*- coding: utf-8 -*

"""
IndividualStarView type's DAO
"""

import sqlite3

from .IndividualStarViewRecord import IndividualStarViewRecord


class IndividualStarViewDAO:

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    # Retrieving star view records from the database
    def getIndividualStarViewRecords(self):
        individualStarViewRecords = []
        sqlString = 'SELECT submission_id, Star, Title FROM StarView'
        cursor = self.__connection.cursor()
        try:
            cursor.execute(sqlString)
            for row in cursor.fetchall():
                individualStarViewRecords.append(
                    IndividualStarViewRecord(
                        str(row[0]),
                        str(row[1]),
                        str(row[2])
                    )
                )
        except sqlite3.Error(
                "Failed to retrieve star view "
                "records from database"
        ) as er:
            raise er
        finally:
            cursor.close()
        return individualStarViewRecords

    # Closing the database connection
    def __closeConnection(self):
        if self.__connection is not None:
            self.__connection.close()

    # Close the DAO
    def closeDAO(self):
        self.__closeConnection()
