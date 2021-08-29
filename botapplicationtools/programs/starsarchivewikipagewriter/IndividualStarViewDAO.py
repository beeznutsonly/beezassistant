# -*- coding: utf-8 -*

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

        limitString = '' if limit is None else ' LIMIT = {}'.format(
            str(limit)
        )
        sqlString = 'SELECT submission_id, Star, Title FROM StarView{};'.format(
            limitString
        )
        self.__retrieveFromSql(sqlString)

    def retrieveSelected(self, star=None, title=None, limit: int = None):
        if star or title or limit:
            if star or title:
                if star and title:
                    sqlString = 'SELECT submission_id, Star, Title FROM StarView ' \
                                'WHERE star={} AND title={}'.format(star, title)
                elif star:
                    sqlString = 'SELECT submission_id, Star, Title FROM StarView ' \
                                'WHERE star={}'.format(star)
                else:
                    sqlString = 'SELECT submission_id, Star, Title FROM StarView ' \
                                'WHERE title={}'.format(title)
                if limit:
                    sqlString += ' LIMIT = {}'.format(str(limit))

                return self.__retrieveFromSql(sqlString)
            else:
                return self.getIndividualStarViewRecords(limit=limit)
        else:
            return self.getIndividualStarViewRecords()

    def __retrieveFromSql(self, sqlString):
        individualStarViewRecords = []
        cursor = self.__connection.cursor()
        try:
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
