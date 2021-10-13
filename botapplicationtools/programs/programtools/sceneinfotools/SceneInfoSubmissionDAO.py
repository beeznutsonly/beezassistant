# -*- coding: utf-8 -*
from botapplicationtools.programs.programtools.generaltools.SimpleSubmission import SimpleSubmission
from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmission import SceneInfoSubmission


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

    def add(
            self,
            sceneInfoSubmission: SceneInfoSubmission
    ):
        """Inserting new submission data to the database"""

        sqlString = '''
                    INSERT INTO PostInfo (id,Title,TimeCreated)
                    VALUES (%s,%s,%s) ON CONFLICT (id) DO NOTHING;
                    '''
        try:
            self.__cursor.execute(sqlString, (
                sceneInfoSubmission.getSubmissionId,
                sceneInfoSubmission.getTitle,
                sceneInfoSubmission.getTimeCreated
            ))

        # Handle database error
        except Exception as ex:
            raise Exception(
                "Failed to insert a new submission into the database",
                ex
            )

    def remove(
            self,
            submission: SimpleSubmission
    ):
        """Removing submission from the database"""

        sqlString = '''
                    DELETE FROM PostInfo WHERE id = %s;
                    '''
        try:
            self.__cursor.execute(sqlString, (submission.getSubmissionId,))

        # Handle database error
        except Exception as ex:
            raise Exception(
                "Failed to remove the submission from the database",
                ex
            )

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
