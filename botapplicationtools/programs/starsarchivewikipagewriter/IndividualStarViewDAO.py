# -*- coding: utf-8 -*

from typing import Tuple
from .IndividualStarViewRecord import IndividualStarViewRecord


class IndividualStarViewDAO:
    """
    IndividualStarView type's DAO
    """

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def getIndividualStarViewRecords(self, limit: int = None):
        """Retrieving star view records from the database"""

        if limit:
            sqlString = '''
                        SELECT submission_id, Star, Title FROM StarView LIMIT %s;
                        '''
            values = (limit)
        else:
            sqlString = '''
                        SELECT submission_id, Star, Title FROM StarView;  
                        '''
            values = None

        return self.__retrieveFromSql(sqlString, values)

    def retrieveSelected(
        self, 
        star: str = None,
        title: str = None, 
        limit: int = None
    ):
        if star or title or limit:
            if star or title:
                values: list
                if star and title:
                    sqlString = 'SELECT submission_id, Star, Title FROM StarView ' \
                                'WHERE Star=%s AND title=%s'
                    values = [star, title]
                elif star:
                    sqlString = 'SELECT submission_id, Star, Title FROM StarView ' \
                                'WHERE Star=%s'
                    values = [star]
                else:
                    sqlString = 'SELECT submission_id, Star, Title FROM StarView ' \
                                'WHERE Title=%s'
                    values = [title]
                if limit:
                    sqlString += ' LIMIT %s'
                    values.append(limit)

                return self.__retrieveFromSql(sqlString, tuple(values))
            else:
                return self.getIndividualStarViewRecords(limit=limit)
        else:
            return self.getIndividualStarViewRecords()

    def __retrieveFromSql(self, sqlString, values: Tuple):
        individualStarViewRecords = []
        cursor = self.__connection.cursor()
        try:
            if values:
                cursor.execute(sqlString, values)
            else:
                cursor.execute(sqlString)
            for row in cursor.fetchall():
                individualStarViewRecords.append(
                    IndividualStarViewRecord(
                        str(row[0]),
                        str(row[1]),
                        str(row[2])
                    )
                )
        except Exception(
                "Failed to retrieve star view "
                "records from database"
        ) as er:
            raise er
        finally:
            cursor.close()
        return individualStarViewRecords
