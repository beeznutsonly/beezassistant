# -*- coding: utf-8 -*-

from botapplicationtools.botcredentials.BotCredentials import BotCredentials


class BotCredentialsDAO:
    """BotCredentials' DAO"""

    __connection = None

    def __init__(self, connection):
        self.__connection = connection

    def saveBotCredentials(
            self,
            botCredentials: BotCredentials,
            connection=__connection
    ):
        """Save bot credentials to database"""

        if connection is None:
            cursor = self.__connection.cursor()
        else:
            cursor = connection.cursor()

        sqlString = (
                'INSERT INTO BotCredentials'
                '(user_agent,client_id,client_secret,'
                'username,password) '
                'VALUES (%s,%s,%s,%s,%s) '
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
                    botCredentials.getUserAgent,
                    botCredentials.getClientId,
                    botCredentials.getClientSecret,
                    botCredentials.getUsername,
                    botCredentials.getPassword
                )
            )
            self.__saveChanges()

        # Handle database error
        except Exception as er:
            raise er
        finally:
            cursor.close()

    def getBotCredentials(
            self, connection=__connection
    ) -> BotCredentials:
        """Retrieving bot credentials from database"""

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

        # Handle if credential retrieval fails
        except Exception(
                "Failed to load bot credentials "
                "from database"
        ) as er:
            raise er
        finally:
            cursor.close()

        return botCredentials

    def __saveChanges(self):
        """Committing any changes to the database"""

        if self.__connection is not None:
            self.__connection.commit()

    def __closeConnection(self):
        """Closing the database connection"""

        if self.__connection is not None:
            self.__connection.close()

    def closeDAO(self):
        """Close the DAO"""

        self.__closeConnection()
