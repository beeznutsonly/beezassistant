# -*- coding: utf-8 -*-

"""
Module responsible for initializing the application's sqlite databases
"""


# Initialize the database
def initializeDatabase(connection, sqlScriptFileName):

    with connection.cursor() as cursor:
        # Reading and executing the sql script file
        with open(sqlScriptFileName) as sqlFile:
            sql = sqlFile.read()
        cursor.executescript(sql)
        connection.commit()


