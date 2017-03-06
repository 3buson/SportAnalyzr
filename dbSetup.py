__author__ = '3buson'

import utils
import pyodbc
import traceback
import constants


def main():
    connection = utils.connectToDB()
    cursor     = connection.cursor()

    # DATABASE TABLES
    print "[DB Setup]  Creating empty database tables"

    # SEASONS
    cursor.execute('''
                     CREATE TABLE IF NOT EXISTS seasons (
                        `id` INT NOT NULL,
                        `name` VARCHAR(255),
                        PRIMARY KEY (`id`)
                     );
                   ''')

    # LEAGUES
    cursor.execute('''
                     CREATE TABLE IF NOT EXISTS leagues (
                        `id` INT NOT NULL AUTO_INCREMENT,
                        `acronym` VARCHAR(45),
                        `name` VARCHAR(255),
                        PRIMARY KEY (`id`)
                     );
                   ''')

    # CLUBS
    cursor.execute('''
                     CREATE TABLE IF NOT EXISTS clubs (
                        `id` INT NOT NULL AUTO_INCREMENT,
                        `acronym` VARCHAR(45),
                        `name` VARCHAR(255),
                        `league_id` INT,
                        PRIMARY KEY (`id`),
                        CONSTRAINT fk_clubs_league_id FOREIGN KEY (`league_id`) REFERENCES `leagues`(`id`)
                     );
                   ''')

    # MATCHES
    cursor.execute('''
                     CREATE TABLE IF NOT EXISTS matches (
                        `id` INT NOT NULL AUTO_INCREMENT,
                        `season_id` INT,
                        `league_id` INT,
                        `date` DATE,
                        `stage` VARCHAR(255),
                        `home_club_id` INT,
                        `away_club_id` INT,
                        `home_score` INT,
                        `away_score` INT,
                        `home_odds` FLOAT,
                        `away_odds` FLOAT,
                        `home_odds_prog` FLOAT,
                        `away_odds_prog` FLOAT,
                        `extra_time` TINYINT,
                        PRIMARY KEY (`id`),
                        INDEX `k_matches_extra_time` (`extra_time`),
                        CONSTRAINT fk_matches_season_id FOREIGN KEY (`season_id`) REFERENCES `seasons`(`id`),
                        CONSTRAINT fk_matches_league_id FOREIGN KEY (`league_id`) REFERENCES `leagues`(`id`),
                        CONSTRAINT fk_matches_home_club_id FOREIGN KEY (`home_club_id`) REFERENCES `clubs`(`id`),
                        CONSTRAINT fk_matches_away_club_id FOREIGN KEY (`away_club_id`) REFERENCES `clubs`(`id`)
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


    # LEAGUES
    print "[DB Setup]  Inserting leagues"

    for leagueAcronym, leagueName in constants.leagues.iteritems():
        try:
            cursor.execute('''
                             INSERT IGNORE INTO leagues(acronym, name)
                             VALUES (?, ?)
                           ''',
                           leagueAcronym, leagueName)
        except pyodbc.DatabaseError, e:
            print "[DB Setup]  ERROR - DatabaseError", e
            traceback.print_exc()

    connection.commit()


    # CLUBS
    print "[DB Setup]  Inserting clubs"

    for league, clubsDict in constants.clubs.iteritems():
        print "[DB Setup]  Inserting %s clubs" % league

        for club, clubName in clubsDict.iteritems():
            try:
                cursor.execute('''
                            SELECT id FROM leagues
                            WHERE leagues.acronym = "%s"
                          ''' %
                          league)

                leagueId = cursor.fetchall()[0][0]

                cursor.execute('''
                                 INSERT IGNORE INTO clubs(acronym, name, league_id)
                                 VALUES (?, ?, ?)
                               ''',
                               club, clubName, leagueId)
            except pyodbc.DatabaseError, e:
                print "[DB Setup]  ERROR - DatabaseError", e
                traceback.print_exc()

    connection.commit()

if __name__ == "__main__":
    main()
