# -*- coding: utf-8 -*

class StarInfoReplyerCommentedDAO:
    """
    DAO class responsible for checking for and
    acknowledging comments replied to by the 
    Star Info Replyer
    """

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def acknowledgeComment(self, commentId: str): 
        """Acknowledge the provided comment"""

        sqlString = "INSERT INTO StarInfoReplyerCommented(commentId)" \
                    " VALUES (%s) ON CONFLICT DO NOTHING;"

        cursor = self.__connection.cursor()
        try:
            cursor.execute(sqlString, (commentId,))
            self.__connection.commit()
        finally:
            cursor.close()

    def checkExists(self, commentId: str) -> bool:
        """
        Check if provided comment exists in
        storage
        """

        sqlString = 'SELECT commentId FROM ' \
                    'StarInfoReplyerCommented ' \
                    'WHERE commentId=%s;'

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString, (commentId,))
            return bool(cursor.fetchone())
        finally:
            cursor.close()
