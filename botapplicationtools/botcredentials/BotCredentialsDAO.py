# -*- coding: utf-8 -*-

"""
BotCredentials' sqlite DAO
"""

import sqlite3

from botapplicationtools.botcredentials.BotCredentials import BotCredentials


class BotCredentialsDAO:

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    # Save bot credentials to database
    def saveBotCredentials(
            self,
            botCredentials,
            connection=__connection
    ):

        if connection is None:
            cursor = self.__connection.cursor()
        else:
            cursor = connection.cursor()

        sqlString = (
                'INSERT INTO BotCredentials'
                '(user_agent,client_id,client_secret,'
                'username,password) '
                'VALUES (?,?,?,?,?) '
                'ON CONFLICT'
                '(client_id,client_secret) '
                'DO '
                'UPDATE SET '
                'user_agent=excluded.user_agent, '
                'username=excluded.username, '
                'password=excluded.password'
        )
        try:
            cursor.execute(
                sqlString, (
                    botCredentials.getUserAgent(),
                    botCredentials.getClientId(),
                    botCredentials.getClientSecret(),
                    botCredentials.getUsername(),
                    botCredentials.getPassword()
                )
            )
            self.__saveChanges()

        # Handle database error
        except sqlite3.DatabaseError as er:
            raise er

    # Retrieving bot credentials from database
    def getBotCredentials(self, connection=__connection):

        sqlString = 'SELECT user_agent, client_id, client_secret,' \
                    ' username, password FROM BotCredentials'

        cursor = connection.cursor() \
            if connection is not None \
            else self.__connection.cursor()

        try:
            cursor.execute(sqlString)
            credentials = cursor.fetchone()

            if credentials is not None:
                botCredentials = BotCredentials(
                    str(credentials[0]),
                    str(credentials[1]),
                    str(credentials[2]),
                    str(credentials[3]),
                    str(credentials[4]),
                )
            else:
                botCredentials = BotCredentials(
                    '', '', '', '', ''
                )

        # Handle of credential retrieval fails
        except sqlite3.DatabaseError(
                "Failed to load bot credentials "
                "from database"
        ) as er:
            raise er
        finally:
            cursor.close()
        return botCredentials

    # Commiting any changes to the database
    def __saveChanges(self):
        if self.__connection is not None:
            self.__connection.commit()

    # Closing the database connection
    def __closeConnection(self):
        if self.__connection is not None:
            self.__connection.close()

    # Close the DAO
    def closeDAO(self):
        self.__closeConnection()
