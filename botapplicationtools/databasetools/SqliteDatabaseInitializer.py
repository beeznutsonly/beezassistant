# -*- coding: utf-8 -*-

"""
Module responsible for initializing the application's sqlite databases
"""

import sqlite3


# Initialize the database
def initializeDatabase(databaseString, sqlScriptFileName):

    # Creating and connecting to database file
    connection = sqlite3.connect(databaseString)
    cursor = connection.cursor()

    # Reading and executing the sql script file
    sqlFile = open(sqlScriptFileName)
    sql = sqlFile.read()
    sqlFile.close()
    cursor.executescript(sql)
    connection.commit()
    cursor.close()
    connection.close()


