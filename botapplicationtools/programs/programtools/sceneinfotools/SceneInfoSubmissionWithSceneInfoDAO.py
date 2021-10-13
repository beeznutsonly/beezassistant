# -*- coding: utf-8 -*

from botapplicationtools.programs.programtools.sceneinfotools\
    .SceneInfoSubmissionWithSceneInfo import SceneInfoSubmissionWithSceneInfo


class SceneInfoSubmissionWithSceneInfoDAO:
    """
    SceneInfoSubmissionWithSceneInfo type's DAO
    """

    __connection = None
    __cursor = None

    def __init__(self, connection):
        self.__connection = connection
        self.__cursor = connection.cursor()

    def add(
        self, 
        sceneInfoSubmissionWithSceneInfo:
        SceneInfoSubmissionWithSceneInfo
    ):
        """
        Inserting new submission and scene info data
        to the database
        """

        sqlString = '''
                    INSERT INTO SubmissionsAndInfo(submission_id,Movie,Star1,Star2)
                    VALUES (%s,%s,%s,%s) ON CONFLICT(submission_id) DO
                    UPDATE SET 
                    Movie=excluded.Movie, Star1=excluded.Star1, Star2=excluded.Star2;
                    '''
        try:
            self.__cursor.execute(sqlString,
                (
                    sceneInfoSubmissionWithSceneInfo
                        .getSceneInfoSubmission
                        .getSubmissionId,

                    sceneInfoSubmissionWithSceneInfo
                        .getSceneInfo.getMovieName,

                    sceneInfoSubmissionWithSceneInfo
                        .getSceneInfo.getStars[0],

                    sceneInfoSubmissionWithSceneInfo
                        .getSceneInfo.getStars[1]
                )
            )
        except Exception as ex:
            raise Exception(
                "Failed to insert new submission and "
                "scene info data into the database",
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
        """Close cursor"""

        if self.__cursor is not None:
            self.__cursor.close()

    def closeConnection(self):
        """Close connection to database"""

        if self.__connection is not None:
            self.__connection.close()

    def closeDAO(self):
        """Closing the DAO"""

        self.closeCursor()
        self.closeConnection()
