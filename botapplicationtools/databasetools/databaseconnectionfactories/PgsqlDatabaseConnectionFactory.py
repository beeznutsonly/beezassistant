# -*- coding: utf-8 -*

import psycopg2
from psycopg2 import pool

from botapplicationtools.databasetools.databaseconnectionfactories \
    .DatabaseConnectionFactory import DatabaseConnectionFactory
from botapplicationtools.databasetools.exceptions.DatabaseConnectionFailureError import DatabaseConnectionFailureError
from botapplicationtools.databasetools.exceptions.DatabaseNotFoundError \
    import DatabaseNotFoundError


class PgsqlDatabaseConnectionFactory(DatabaseConnectionFactory):
    """
    Connection Factory for the bot application's PostgresSQL database
    """

    __connectionPool: pool.ThreadedConnectionPool

    def __init__(self, connectionPool):
        self.__connectionPool = connectionPool

    def getConnection(self):
        if self.__connectionPool.closed:
            raise DatabaseConnectionFailureError(
                "The connection factory is closed"
            )
        return self.__connectionPool.getconn()

    def yieldConnection(self, connection):
        self.__connectionPool.putconn(connection)

    def shutDown(self):
        self.__connectionPool.closeall()

    @classmethod
    def __databaseExists(
        cls,
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
                # Retrieve list of all databases on the cluster
                cursor = connection.cursor()
                cursor.execute("SELECT datname FROM pg_database;")
                databaseList = cursor.fetchall()
                return (databaseName,) in databaseList
            finally:
                cursor.close()

    @classmethod
    def getFactoryFromCredentials(
        cls,
        databaseName: str,
        user: str,
        password: str,
        host='localhost', 
        port='5432'
    ):
        """
        Create a Database Connection Factory using
        the provided database credentials. Raises
        a DatabaseNotFoundError if the provided
        database is not found on the cluster
        """

        # Check for existence of database first
        if not cls.__databaseExists(
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

        return PgsqlDatabaseConnectionFactory(
            pool.ThreadedConnectionPool(
                5, 20,
                dbname=databaseName,
                user=user,
                password=password,
                host=host,
                port=port
            )
        )

    @classmethod
    def getFactoryFromDsn(cls, dsn: str):
        """
        Create a Database Connection Factory using
        the provided dsn
        """

        return PgsqlDatabaseConnectionFactory(
            pool.ThreadedConnectionPool(5, 20, dsn)
        )
