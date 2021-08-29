# -*- coding: utf-8 -*

class StarInfoReplyerCommentedDAO:

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def acknowledgeComment(self, commentId):

        sqlString = "INSERT INTO StarInfoReplyerCommented(commentId)" \
                    " VALUES {};".format(commentId)

        cursor = self.__connection.cursor()
        try:
            cursor.execute(sqlString)
            self.__connection.commit()
        finally:
            cursor.close()

    def checkExists(self, commentId) -> bool:

        sqlString = "SELECT commentId from StarInfoReplyerCommented" \
                    "WHERE commentId = {};".format(commentId)

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString)
            result = cursor.fetchall()
            return commentId in result
        finally:
            cursor.close()
