# -*- coding: utf-8 -*

class SceneInfoSubmissionDAO:
    """
    Class representing a SceneInfoSubmission
    (currently just wrapper for a PRAW Submission)
    type's DAO
    """

    __connection = None
    __cursor = None

    def __init__(self, connection):
        self.__connection = connection
        self.__cursor = connection.cursor()

    def add(self, sceneInfoSubmission):
        """Inserting new submission data to the database"""

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
        except Exception(
                "Failed to insert a new submission into the database"
        ) as er:
            raise er

    def refreshCursor(self):
        """Reset cursor for the DAO"""

        self.closeCursor()
        self.__cursor = self.__connection.cursor()

    def saveChanges(self):
        """Committing any changes to the database"""

        if self.__connection is not None:
            self.__connection.commit()
            self.refreshCursor()

    def closeCursor(self):
        """Closing the cursor"""

        if self.__cursor is not None:
            self.__cursor.close()

    def closeConnection(self):
        """Closing the database connection"""

        if self.__connection is not None:
            self.__connection.close()

    def closeDAO(self):
        """Closing the database connection"""

        self.closeCursor()
        self.closeConnection()
