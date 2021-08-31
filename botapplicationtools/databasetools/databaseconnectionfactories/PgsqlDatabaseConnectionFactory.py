# -*- coding: utf-8 -*

import psycopg2
from psycopg2 import pool

from botapplicationtools.databasetools.databaseconnectionfactories \
    .DatabaseConnectionFactory import DatabaseConnectionFactory
from botapplicationtools.databasetools.exceptions.DatabaseNotFoundError \
    import DatabaseNotFoundError


class PgsqlDatabaseConnectionFactory(DatabaseConnectionFactory):
    """
    Connection Factory for the bot application's PostgresSQL database
    """

    __connectionPool: pool.ThreadedConnectionPool

    def __init__(
        self, user, password, databaseName, 
        host='localhost', port='5432'
    ):

        if not self.__databaseExists(
            databaseName, 
            user,
            password,
            host,
            port
        ):
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
            host=host,
            port=port,
            dbname=databaseName
        )

    def getConnection(self):
        return self.__connectionPool.getconn()

    @staticmethod
    def __databaseExists(
        databaseName, 
        user,
        password,
        host,
        port
    ):
        """
        Convenience method to check the existence
        of the given database
        """

        if databaseName is None or databaseName == '':
            return False

        with psycopg2.connect(
            user=user, password=password, 
            host=host, port=port
        ) as connection:

            connection.autocommit = True
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT datname FROM pg_database;")
                databaseList = cursor.fetchall()
                return (databaseName,) in databaseList
            finally:
                cursor.close()
