class SubmissionReplyerCommentedDAO:
    """
    """

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def acknowledgeSubmission(self, submissionId):
        sqlString = "INSERT INTO SubmissionReplyerCommented(submissionId)" \
                    " VALUES {};".format(submissionId)

        cursor = self.__connection.cursor()
        try:
            cursor.execute(sqlString)
            self.__connection.commit()
        finally:
            cursor.close()

    def checkExists(self, submissionId) -> bool:

        sqlString = "SELECT submissionId from SubmissionReplyerCommented" \
                    "WHERE submissionId = {};".format(submissionId)

        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString)
            result = cursor.fetchall()
            return submissionId in result
        finally:
            cursor.close()
