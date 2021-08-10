# -*- coding: utf-8 -*

"""
SceneInfoSubmissionWithSceneInfo type's sqlite DAO
"""

import sqlite3


class SceneInfoSubmissionWithSceneInfoDAO:

    __connection = None
    __cursor = None

    def __init__(self, connection):
        self.__connection = connection
        self.__cursor = connection.cursor()

    # Inserting new submission and scene info data
    # to the database
    def add(self, sceneInfoSubmissionWithSceneInfo):
        sqlString = '''
                    INSERT INTO SubmissionsAndInfo(submission_id,Movie,Star1,Star2)
                    VALUES (?,?,?,?) ON CONFLICT(submission_id) DO
                    UPDATE SET 
                    Movie=excluded.Movie, Star1=excluded.Star1, Star2=excluded.Star2
                    '''
        try:
            self.__cursor.execute(
                sqlString,
                (
                     sceneInfoSubmissionWithSceneInfo
                         .getSceneInfoSubmission().id,

                     sceneInfoSubmissionWithSceneInfo
                         .getSceneInfo().getMovieName(),

                     sceneInfoSubmissionWithSceneInfo
                         .getSceneInfo().getStars()[0],

                     sceneInfoSubmissionWithSceneInfo
                         .getSceneInfo().getStars()[1]
                )
            )
        except sqlite3.Error(
                "Failed to insert new submission and "
                "scene info data into the database"
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

    # Close cursor
    def closeCursor(self):
        if self.__cursor is not None:
            self.__cursor.close()

    # Close connection to database
    def closeConnection(self):
        if self.__connection is not None:
            self.__connection.close()

    # Closing the DAO
    def closeDAO(self):
        self.closeCursor()
        self.closeConnection()
