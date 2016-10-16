__author__ = '3buson'

import sys
import utils
import pyodbc
import traceback

sys.path.insert(0, '../')
import constants


def main():
    connection = utils.connectToDB()
    cursor     = connection.cursor()

    # DATABASE TABLES
    print "[DB Setup]  Creating empty database tables"

    # SEASONS
    cursor.execute('''
                     CREATE TABLE IF NOT EXISTS seasons (
                        id INT,
                        name VARCHAR(255),
                        PRIMARY KEY (id)
                     );
                   ''')

    # LEAGUES
    cursor.execute('''
                     CREATE TABLE IF NOT EXISTS leagues (
                        id INT,
                        acronym VARCHAR(45),
                        name VARCHAR(255),
                        PRIMARY KEY (id)
                     );
                   ''')

    # CLUBS
    cursor.execute('''
                     CREATE TABLE IF NOT EXISTS clubs (
                        id INT,
                        acronym VARCHAR(45),
                        name VARCHAR(255),
                        league_id INT,
                        PRIMARY KEY (id),
                        CONSTRAINT fk_league_id FOREIGN KEY (league_id) REFERENCES leagues(id)
                     );
                   ''')

    connection.commit()

    # SEASONS
    print "[DB Setup]  Inserting seasons"

    for i in xrange(1976, 2016):
        try:
            cursor.execute('''
                             INSERT IGNORE INTO seasons(id, name)
                             VALUES (?, ?)
                           ''',
                           i, i)
        except pyodbc.DatabaseError, e:
            print "[DB Setup]  ERROR - DatabaseError", e
            traceback.print_exc()

    connection.commit()


    # LEAGUES
    print "[DB Setup]  Inserting leagues"

    id = 0
    for leagueAcronym, leagueName in constants.leagues.iteritems():
        try:
            cursor.execute('''
                             INSERT IGNORE INTO leagues(id, acronym, name)
                             VALUES (?, ?, ?)
                           ''',
                           id, leagueAcronym, leagueName)
        except pyodbc.DatabaseError, e:
            print "[DB Setup]  ERROR - DatabaseError", e
            traceback.print_exc()

        id += 1


    # CLUBS
    print "[DB Setup]  Inserting clubs"

    for league, clubsDict in constants.clubs.iteritems():
        print "[DB Setup]  Inserting %s clubs" % league

        id = 0
        for club, clubName in clubsDict.iteritems():
            try:
                cursor.execute('''
                            SELECT id FROM leagues
                            WHERE leagues.acronym = '%s'
                          ''' %
                          league)

                leagueId = cursor.fetchall()[0][0]

                cursor.execute('''
                                 INSERT IGNORE INTO clubs(id, acronym, name, league_id)
                                 VALUES (?, ?, ?, ?)
                               ''',
                               id, club, clubName, leagueId)
            except pyodbc.DatabaseError, e:
                print "[DB Setup]  ERROR - DatabaseError", e
                traceback.print_exc()

            id += 1

    connection.commit()

if __name__ == "__main__":
    main()
