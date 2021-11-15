# -*- coding: utf-8 -*

from typing import Tuple, List

from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmission import SceneInfoSubmission
from .StarPairSceneInfoSubmissionDetail import StarPairSceneInfoSubmissionDetail


class StarPairSceneInfoSubmissionDetailDAO:
    """
    Class representing a StarPairSceneInfoSubmissionDetail's DAO
    """

    def __init__(self, connection):
        self.__connection = connection

    def retrieveAll(
            self,
            limit: int = None
    ) -> List[StarPairSceneInfoSubmissionDetail]:
        """Retrieve StarPairSceneInfoSubmissions from the database"""

        if limit:
            sqlString = '''
                        SELECT submission_id, star1, star2, Title, Movie FROM StarPairView LIMIT %s;
                        '''
            values = (limit,)
        else:
            sqlString = '''
                        SELECT submission_id, star1, star2, Title, Movie FROM StarPairView;  
                        '''
            values = None

        return self.__retrieveFromSql(sqlString, values)

    def retrieveSelected(
        self,
        star1: str = None,
        star2: str = None,
        limit: int = None
    ) -> List[StarPairSceneInfoSubmissionDetail]:
        """
        Retrieve StarPairSceneInfoSubmissionDetails according to
        the given arguments
        """

        if star1 or star2 or limit:
            if star1 or star2:
                values: list
                if star1 and star2:
                    sqlString = 'SELECT submission_id, star1, star2, Title, Movie FROM StarPairView ' \
                                'WHERE (star1=%s AND star2=%s) OR (star2=%s AND star1=%s)'
                    values = [star1, star2, star2, star1]
                elif star1:
                    sqlString = 'SELECT submission_id, star1, star2, Title, Movie FROM StarPairView ' \
                                'WHERE star1=%s OR star2=%s'
                    values = [star1, star1]
                else:
                    sqlString = 'SELECT submission_id, star1, star2, Title, Movie FROM StarPairView ' \
                                'WHERE star1=%s OR star2=%s'
                    values = [star2, star2]
                if limit:
                    sqlString += ' LIMIT %s'
                    values.append(limit)

                sqlString += ";"

                return self.__retrieveFromSql(sqlString, tuple(values))
            else:
                return self.retrieveAll(limit=limit)
        else:
            return self.retrieveAll()

    def __retrieveFromSql(
            self, sqlString: str, values: Tuple
    ) -> List[StarPairSceneInfoSubmissionDetail]:

        starPairSceneInfoSubmissionDetails = []
        cursor = self.__connection.cursor()
        try:
            if values:
                cursor.execute(sqlString, values)
            else:
                cursor.execute(sqlString)
            for row in cursor.fetchall():
                starPairSceneInfoSubmissionDetails.append(
                    StarPairSceneInfoSubmissionDetail(
                        (row[1], row[2]),
                        SceneInfoSubmission(
                            str(row[0]),
                            str(row[3]),
                            None,
                            str(row[4])
                        )
                    )
                )
        except Exception as ex:
            raise Exception(
                "Failed to retrieve star pair scene info submission "
                "details from the database",
                ex
            )
        finally:
            cursor.close()
        return starPairSceneInfoSubmissionDetails
