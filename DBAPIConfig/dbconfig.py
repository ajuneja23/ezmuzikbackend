import sqlite3


def getDBConnection():
    connection = sqlite3.connect('spotifystats.db')
    return connection
