# -*- coding: utf-8 -*

"""
Class representing a SceneInfoSubmission
(currently just wrapper for a PRAW Submission)
type's sqlite DAO
"""

import sqlite3


class SceneInfoSubmissionDAO:

    __connection = None
    __cursor = None

    def __init__(self, connection):
        self.__connection = connection
        self.__cursor = connection.cursor()

    # Inserting new submission data to the database
    def add(self, sceneInfoSubmission):
        sqlString = '''
                    INSERT OR IGNORE INTO PostInfo (id,Title,TimeCreated)
                    VALUES (?,?,?)
                    '''
        try:
            self.__cursor.execute(
                sqlString,
                (
                    sceneInfoSubmission.id,
                    sceneInfoSubmission.title,
                    sceneInfoSubmission.created_utc
                )
            )

        # Handle database error
        except sqlite3.DatabaseError(
                "Failed to insert a new submission into the database"
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

    # Closing the database connection
    def closeConnection(self):
        if self.__connection is not None:
            self.__connection.close()

    # Closing the DAO
    def closeDAO(self):
        self.closeCursor()
        self.closeConnection()
