# -*- coding: utf-8 -*-

"""
Module responsible for initializing the application's database
"""


def initializeDatabase(connection, sqlScriptFileName):
    """Initialize the database"""

    cursor = connection.cursor()
    # Reading and executing the sql script file
    with open(sqlScriptFileName) as sqlFile:
        sql = sqlFile.read()
    cursor.executescript(sql)
    connection.commit()
    cursor.close()


