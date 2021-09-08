# -*- coding: utf-8 -*

from botapplicationtools.programs.programtools.sceneinfotools.SimpleSceneInfo \
    import SimpleSceneInfo


class SimpleSceneInfoDAO:
    """SceneInfo type's DAO"""

    __connection = None
    __cursor = None

    def __init__(self, connection):
        self.__connection = connection
        self.__cursor = connection.cursor()

    def add(self, sceneInfo: SimpleSceneInfo):
        """Inserting new scene info data into database"""

        sqlString = (
            'INSERT INTO SceneInfo(Movie,Star1,Star2) ' +
            'VALUES (%s,%s,%s) ON CONFLICT DO NOTHING'
        )
        try:
            self.__cursor.execute(
                sqlString, (
                    sceneInfo.getMovieName,
                    sceneInfo.getStars[0],
                    sceneInfo.getStars[1]
                )
            )

        # Handle database error
        except Exception as er:
            raise Exception(
                "Failed to insert new scene info "
                "into the database",
                er
            )

    def add(self, sceneInfo: SimpleSceneInfo):
        """Inserting new scene info data into database"""

        sqlString = (
            'INSERT INTO SceneInfo(Movie,Star1,Star2) ' +
            'VALUES (%s,%s,%s) ON CONFLICT DO NOTHING'
        )
        try:
            self.__cursor.execute(
                sqlString, (
                    sceneInfo.getMovieName,
                    sceneInfo.getStars[0],
                    sceneInfo.getStars[1]
                )
            )

        # Handle database error
        except Exception as er:
            raise Exception(
                "Failed to insert new scene info "
                "into the database",
                er
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
        """Close the database connection"""

        if self.__connection is not None:
            self.__connection.close()

    def closeDAO(self):
        """Closing the DAO"""

        self.closeCursor()
        self.closeConnection()
