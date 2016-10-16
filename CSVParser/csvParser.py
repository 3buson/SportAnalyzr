__author__ = '3buson'

import csv
import sys

from Match import Match

sys.path.insert(0, '../')
import utils

csvPath     = '../FileConqueror/csv/'
csvFilename = 'NBA1976-2014.csv'

connection = utils.connectToDB()
cursor     = connection.cursor()

rownum = 0
with open(csvPath + csvFilename, 'rb') as f:
    reader = csv.reader(f, delimiter=';')

    for row in reader:
        if rownum == 0:
            header = row

            rownum += 1
        else:
            leagueAcronym = row[1]
            seasonId      = row[3]
            date          = row[5]
            homeClubName  = row[6]
            awayClubName  = row[7]
            homeClubScore = row[8]
            awayClubScore = row[9]
            extraTime     = row[10]
            homeOdds      = row[11] if row[11] != 'NA' else -1
            awayOdds      = row[12] if row[12] != 'NA' else -1
            homeOddsProg  = row[13] if row[13] != 'NA' else -1
            awayOddsProg  = row[14] if row[14] != 'NA' else -1

            cursor.execute('''
                            SELECT id FROM leagues
                            WHERE leagues.acronym = '%s'
                          ''' %
                          leagueAcronym)
            leagueId = cursor.fetchall()[0][0]

            cursor.execute('''
                            SELECT id FROM clubs
                            WHERE clubs.name LIKE '%s'
                          ''' %
                          homeClubName)
            homeClubId = cursor.fetchall()[0][0]

            cursor.execute('''
                            SELECT id FROM clubs
                            WHERE clubs.name LIKE '%s'
                          ''' %
                          awayClubName)
            awayClubId = cursor.fetchall()[0][0]

            match = Match(seasonId, leagueId, date, homeClubId, awayClubId,
                          homeClubScore, awayClubScore, homeOdds, awayOdds,
                          homeOddsProg, awayOddsProg, extraTime)

            if rownum % 500 == 0:
                print "[CSV Parser]  Inserting match %d..." % rownum

            match.dbInsert(connection)

            rownum += 1
