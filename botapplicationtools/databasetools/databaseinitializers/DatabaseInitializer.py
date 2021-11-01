# -*- coding: utf-8 -*-

"""
Module responsible for initializing the application's database
"""


def initializeDatabase(connection, database, sqlScriptFileName):
    """Initialize the database"""

    cursor = connection.cursor()

    # Reading and executing the sql script file
    with open(sqlScriptFileName) as sqlFile:
        sql = sqlFile.read()
    if database == 'sqlite':
        cursor.executescript(sql)
        connection.commit()
    else:
        connection.autocommit = True
        cursor.execute(sql)
        cursor.close()


