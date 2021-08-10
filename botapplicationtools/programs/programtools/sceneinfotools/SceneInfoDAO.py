# -*- coding: utf-8 -*

"""
SceneInfo type's sqlite DAO
"""

import sqlite3


class SceneInfoDAO:

    __connection = None
    __cursor = None

    def __init__(self, connection):
        self.__connection = connection
        self.__cursor = connection.cursor()

    # Inserting new scene info data into database
    def add(self, sceneInfo):
        sqlString = (
            'INSERT INTO SceneInfo(Movie,Star1,Star2) ' +
            'VALUES (?,?,?) ON CONFLICT DO NOTHING'
        )
        try:
            self.__cursor.execute(
                sqlString, (
                    sceneInfo.getMovieName(), 
                    sceneInfo.getStars()[0], 
                    sceneInfo.getStars()[1]
                )
            )

        # Handle database error
        except sqlite3.Error(
                "Failed to insert new scene info "
                "into the database"
        ) as er:
            raise er

    # Reset cursor for the DAO
    def refreshCursor(self):
        self.closeCursor()
        self.__cursor = self.__connection.cursor()

    # Commiting any changes to the database
    def saveChanges(self):
        if self.__connection is not None:
            self.__connection.commit()
            self.refreshCursor()

    # Closing the cursor
    def closeCursor(self):
        if self.__cursor is not None:
            self.__cursor.close()

    # Close the database connection
    def closeConnection(self):
        if self.__connection is not None:
            self.__connection.close()

    # Closing the DAO
    def closeDAO(self):
        self.closeCursor()
        self.closeConnection()
