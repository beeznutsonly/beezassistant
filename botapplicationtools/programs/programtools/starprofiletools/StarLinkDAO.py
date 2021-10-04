from typing import List

from botapplicationtools.programs.programtools.starprofiletools.Star import Star
from botapplicationtools.programs.programtools.starprofiletools.StarLink import StarLink


class StarLinkDAO:

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def getStarLinks(self, star: Star) -> List[StarLink]:

        sqlString = "SELECT link, link_name FROM StarLink WHERE name = %s;"
        cursor = self.__connection.cursor()

        try:
            cursor.execute(sqlString, (star.getName,))
            results = cursor.fetchall()
            starLinks = []
            for record in results:
                starLinks.append(StarLink(
                    star,
                    record[0],
                    record[1]
                ))
            return starLinks

        finally:
            cursor.close()
