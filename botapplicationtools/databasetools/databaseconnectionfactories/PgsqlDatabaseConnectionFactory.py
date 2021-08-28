import psycopg2
from psycopg2 import pool

from botapplicationtools.databasetools.databaseconnectionfactories.DatabaseConnectionFactory import \
    DatabaseConnectionFactory
from botapplicationtools.databasetools.exceptions.DatabaseNotFoundError import DatabaseNotFoundError


class PgsqlDatabaseConnectionFactory(DatabaseConnectionFactory):

    __connectionPool: pool.ThreadedConnectionPool

    def __init__(self, user, password, databaseName):

        if not self.__databaseExists(databaseName):
            raise DatabaseNotFoundError(
                'The provided database, "{}", '
                'does not exist'.format(
                    databaseName
                )
            )

        self.__connectionPool = pool.ThreadedConnectionPool(
            5, 20,
            user=user,
            password=password,
            dbName=databaseName
        )

    def getConnection(self):
        return self.__connectionPool.getconn()

    @classmethod
    def __databaseExists(cls, databaseName):

        if databaseName is None or databaseName == '':
            return False

        with psycopg2.connect(
                "user='postgres' "
                "host='localhost' "
                "password='postgres' "
                "port='5432'"
        ) as connection:

            connection.autocommit = True
            with connection.cursor() as cursor:
                cursor.execute("SELECT datname FROM pg_database;")
                databaseList = cursor.fetchall()

                return databaseName in databaseList