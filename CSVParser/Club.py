__author__ = '3buson'

import pyodbc
import traceback


class Club:
    def __init__(self, acronym=None, name=None, leagueId=None):
        self.id       = id
        self.acronym  = acronym
        self.name     = name
        self.leagueId = leagueId

    def dbInsert(self, connection):
        cursor = connection.cursor()

        try:
            cursor.execute('''
                            INSERT IGNORE INTO clubs(acronym, name, league_id)
                            VALUES (?, ?, ?)
                           ''',
                           self.acronym, self.name, self.leagueId)

        except pyodbc.DatabaseError, e:
            print "[Club class]  ERROR - DatabaseError", e
            traceback.print_exc()

        connection.commit()