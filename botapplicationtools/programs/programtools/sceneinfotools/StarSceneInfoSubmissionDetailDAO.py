# -*- coding: utf-8 -*

from botapplicationtools.programs.programtools.sceneinfotools.SceneInfoSubmission import SceneInfoSubmission
from typing import Tuple, List
from .StarSceneInfoSubmissionDetail import StarSceneInfoSubmissionDetail


class StarSceneInfoSubmissionDetailDAO:
    """
    Class representing a StarSceneInfoSubmissionDetail's DAO
    """

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def retrieveAll(
            self,
            limit: int = None
    ) -> List[StarSceneInfoSubmissionDetail]:
        """Retrieve StarSceneInfoSubmissions from the database"""

        if limit:
            sqlString = '''
                        SELECT submission_id, Star, Title, Movie FROM StarView LIMIT %s;
                        '''
            values = (limit,)
        else:
            sqlString = '''
                        SELECT submission_id, Star, Title, Movie FROM StarView;  
                        '''
            values = None

        return self.__retrieveFromSql(sqlString, values)

    def retrieveSelected(
        self, 
        star: str = None,
        title: str = None, 
        limit: int = None
    ) -> List[StarSceneInfoSubmissionDetail]:
        """
        Retrieve StarSceneInfoSubmissionDetails according to
        the given arguments
        """

        if star or title or limit:
            if star or title:
                values: list
                if star and title:
                    sqlString = 'SELECT submission_id, Star, Title, Movie FROM StarView ' \
                                'WHERE Star=%s AND Title=%s'
                    values = [star, title]
                elif star:
                    sqlString = 'SELECT submission_id, Star, Title, Movie FROM StarView ' \
                                'WHERE Star=%s'
                    values = [star]
                else:
                    sqlString = 'SELECT submission_id, Star, Title, Movie FROM StarView ' \
                                'WHERE Title=%s'
                    values = [title]
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
    ) -> List[StarSceneInfoSubmissionDetail]:

        starSceneInfoSubmissionDetails = []
        cursor = self.__connection.cursor()
        try:
            if values:
                cursor.execute(sqlString, values)
            else:
                cursor.execute(sqlString)
            for row in cursor.fetchall():
                starSceneInfoSubmissionDetails.append(
                    StarSceneInfoSubmissionDetail(
                        str(row[1]), 
                        SceneInfoSubmission(
                            str(row[0]),
                            str(row[2]),
                            None,
                            str(row[3])
                        )
                    )
                )
        except Exception as ex:
            raise Exception(
                "Failed to retrieve star scene info submission "
                "details from the database",
                ex
            )
        finally:
            cursor.close()
        return starSceneInfoSubmissionDetails
