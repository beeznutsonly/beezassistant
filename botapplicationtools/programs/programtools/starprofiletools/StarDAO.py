from botapplicationtools.programs.programtools.starprofiletools.Star import Star


class StarDAO:

    __connection = None
    
    def __init__(self, connection):
        self.__connection = connection

    def getStar(self, name: str) -> Star:
        cursor = self.__connection.cursor()
        sqlString = '''
                    SELECT
                        name, 
                        birthday, 
                        nationality,
                        birth_place,
                        years_active,
                        description 
                    FROM Star
                    WHERE name = %s;
                    '''
        try:
            cursor.execute(sqlString, (name,))
            result = cursor.fetchone()
            star = None
            if result:
                star = Star(
                    result[0],
                    result[1],
                    result[2],
                    result[3],
                    result[4],
                    result[5]
                )
            return star
        except Exception as ex:
            raise Exception(
                "Failed to retrieve Star information from database",
                ex
            )
        finally:
            cursor.close()

    def getStars(self):
        cursor = self.__connection.cursor()
        sqlString = '''
                    SELECT
                        name, 
                        birthday, 
                        nationality,
                        birth_place,
                        years_active,
                        description 
                    FROM Star;
                    '''
        try:
            cursor.execute(sqlString)
            results = cursor.fetchAll()
            stars = []
            for record in results:
                stars.append(
                    Star(
                        record[0],
                        record[1],
                        record[2],
                        record[3],
                        record[4],
                        record[5]
                    )
                )
            return stars
        except Exception as ex:
            raise Exception(
                "Failed to retrieve Star information from database",
                ex
            )
        finally:
            cursor.close()

    def checkExists(self, name: str) -> bool:
        try:
            return self.getStar(name) is not None
        except Exception as ex:
            raise Exception(
                "Failed to retrieve Star information from database",
                ex
            )
