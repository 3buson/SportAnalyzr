import csv

import utils

from Club import Club
from Match import Match


__author__ = '3buson'


def parseNBACSVFile(connection, csvFile, delimiter):
    cursor = connection.cursor()

    rownum = 0
    with open(csvFile, 'rb') as f:
        reader = csv.reader(f, delimiter=delimiter)

        for row in reader:
            # skip header
            if rownum == 0:
                rownum += 1
            else:
                leagueAcronym = row[1].strip()
                stage         = row[2]
                seasonId      = row[3]
                date          = row[5]
                homeClubName  = row[6].strip()
                awayClubName  = row[7].strip()
                homeClubScore = row[8]
                awayClubScore = row[9]
                extraTime     = row[10]
                homeOdds      = row[11] if row[11] != 'NA' else -1
                awayOdds      = row[12] if row[12] != 'NA' else -1
                homeOddsProg  = row[13] if row[13] != 'NA' else -1
                awayOddsProg  = row[14] if row[14] != 'NA' else -1

                cursor.execute('''
                                SELECT id FROM leagues
                                WHERE leagues.acronym = "%s"
                              ''' %
                              leagueAcronym)
                leagueId = cursor.fetchall()[0][0]

                cursor.execute('''
                                SELECT id FROM clubs
                                WHERE clubs.name LIKE "%s"
                              ''' %
                              homeClubName)
                homeClubId = cursor.fetchall()[0][0]

                cursor.execute('''
                                SELECT id FROM clubs
                                WHERE clubs.name LIKE "%s"
                              ''' %
                              awayClubName)
                awayClubId = cursor.fetchall()[0][0]

                match = Match(seasonId, leagueId, date, stage,
                              homeClubId, awayClubId, homeClubScore, awayClubScore,
                              homeOdds, awayOdds, homeOddsProg, awayOddsProg,
                              extraTime)

                if rownum % 500 == 0:
                    print "[CSV Parser]  Inserting match %d..." % rownum

                match.dbInsert(connection)

                rownum += 1


def parseFootballCSVFile(connection, csvFile, delimiter):
    cursor = connection.cursor()

    rownum = 0
    with open(csvFile, 'rb') as f:
        reader = csv.reader(f, delimiter=delimiter)

        for row in reader:
            # skip header
            if rownum == 0:
                rownum += 1
            else:
                leagueAcronym = row[0].strip()
                season        = row[1]
                date          = row[2]
                homeClubName  = row[3].strip()
                awayClubName  = row[4].strip()
                homeClubScore = row[5]
                awayClubScore = row[6]

                seasonId  = str(int(season[-2:]) + 2000 - 1)
                stage     = 'regular'
                extraTime = 0

                dateArray = date.split('/')
                dateArray.reverse()

                date = '-'.join(dateArray)
                date = '20' + date

                cursor.execute('''
                                SELECT id FROM leagues
                                WHERE leagues.acronym = "%s"
                              ''' %
                               leagueAcronym)
                leagueId = cursor.fetchall()[0][0]

                cursor.execute('''
                                SELECT id FROM clubs
                                WHERE clubs.name = "%s"
                              ''' %
                               homeClubName)

                result = cursor.fetchall()

                # if no such club exists insert it and select again
                if len(result) == 0:
                    homeClub = Club(homeClubName[:3].upper(), homeClubName, leagueId)
                    homeClub.dbInsert(connection)

                    cursor.execute('''
                                    SELECT id FROM clubs
                                    WHERE clubs.name LIKE "%s"
                                  ''' %
                                   homeClubName)
                    homeClubId = cursor.fetchall()[0][0]
                else:
                    homeClubId = result[0][0]

                cursor.execute('''
                                SELECT id FROM clubs
                                WHERE clubs.name LIKE "%s"
                              ''' %
                               awayClubName)

                result = cursor.fetchall()

                # if no such club exists insert it and select again
                if len(result) == 0:
                    awayClub = Club(awayClubName[:3].upper(), awayClubName, leagueId)
                    awayClub.dbInsert(connection)

                    cursor.execute('''
                                SELECT id FROM clubs
                                WHERE clubs.name LIKE "%s"
                              ''' %
                               awayClubName)
                    awayClubId = cursor.fetchall()[0][0]
                else:
                    awayClubId = result[0][0]

                match = Match(seasonId, leagueId, date, stage,
                              homeClubId, awayClubId, homeClubScore, awayClubScore,
                              None, None, None, None,
                              extraTime)

                if rownum % 500 == 0:
                    print "[CSV Parser]  Inserting match %d..." % rownum

                match.dbInsert(connection)

                rownum += 1


def parseVariousSportsCSVFile(connection, csvFile, delimiter):
    cursor = connection.cursor()

    rownum = 0
    with open(csvFile, 'rb') as f:
        reader = csv.reader(f, delimiter=delimiter)

        for row in reader:
            # skip header
            if rownum == 0:
                rownum += 1
            else:
                leagueCode     = row[0].strip()
                season         = row[1].split('_')[1]
                homeClubName   = row[2].strip()
                awayClubName   = row[3].strip()
                homeClubScore  = row[4]
                awayClubScore  = row[5]
                additionalInfo = row[6]
                date           = row[7]

                seasonId  = str(int(season) - 1)
                stage     = 'regular'
                extraTime = 0

                # skip soccer, we get soccer matches from a different source
                if leagueCode.split('.')[0] != 'soccer':
                    leagueAcronym = leagueCode.split('.')[1][:2].upper() + leagueCode.split('.')[0][0].upper()

                    # edge cases
                    if leagueCode == 'handball.portugal.lpa.combined':
                        leagueAcronym = 'PRH'
                    elif leagueCode == 'handball.germany.bundesliga.combined':
                        leagueAcronym = 'GBH'
                    elif leagueCode == 'hockey.switzerland.nla.combined':
                        leagueAcronym = 'CHH'
                    elif leagueCode == 'hockey.usa.nhl.combined':
                        leagueAcronym = 'NHL'

                    if additionalInfo == 'ET' or additionalInfo == 'pen.'   :
                        extraTime = 1

                    dateArray = date.split('.')
                    dateArray.reverse()

                    date = '-'.join(dateArray)

                    cursor.execute('''
                                    SELECT id FROM leagues
                                    WHERE leagues.acronym = "%s"
                                  ''' %
                                   leagueAcronym)
                    try:
                        leagueId = cursor.fetchall()[0][0]
                    except:
                        print leagueAcronym


                    cursor.execute('''
                                    SELECT id FROM clubs
                                    WHERE clubs.name = "%s"
                                  ''' %
                                   homeClubName)

                    result = cursor.fetchall()

                    # if no such club exists insert it and select again
                    if len(result) == 0:
                        homeClub = Club(homeClubName[:3].upper(), homeClubName, leagueId)
                        homeClub.dbInsert(connection)

                        cursor.execute('''
                                        SELECT id FROM clubs
                                        WHERE clubs.name LIKE "%s"
                                      ''' %
                                       homeClubName)
                        homeClubId = cursor.fetchall()[0][0]
                    else:
                        homeClubId = result[0][0]

                    cursor.execute('''
                                    SELECT id FROM clubs
                                    WHERE clubs.name LIKE "%s"
                                  ''' %
                                   awayClubName)

                    result = cursor.fetchall()

                    # if no such club exists insert it and select again
                    if len(result) == 0:
                        awayClub = Club(awayClubName[:3].upper(), awayClubName, leagueId)
                        awayClub.dbInsert(connection)

                        cursor.execute('''
                                    SELECT id FROM clubs
                                    WHERE clubs.name LIKE "%s"
                                  ''' %
                                   awayClubName)
                        awayClubId = cursor.fetchall()[0][0]
                    else:
                        awayClubId = result[0][0]

                    match = Match(seasonId, leagueId, date, stage,
                                  homeClubId, awayClubId, homeClubScore, awayClubScore,
                                  None, None, None, None,
                                  extraTime)

                    if rownum % 500 == 0:
                        print "[CSV Parser]  Inserting match %d..." % rownum

                    match.dbInsert(connection)

                rownum += 1


def main():
    connection = utils.connectToDB()

    csvFilename = raw_input('Please enter CSV filename: ')
    csvPath     = '../FileConqueror/csv/'
    csvFile     = csvPath + csvFilename

    leagueInput = raw_input('Please enter what kind of data CSV file includes [NBA/football/various]: ')

    delimeterInput = raw_input('Please enter the delimeter for this CSV file: ')

    if (leagueInput.lower() == 'nba'):
        parseNBACSVFile(connection, csvFile, delimeterInput)
    elif (leagueInput.lower() == 'football'):
        parseFootballCSVFile(connection, csvFile, delimeterInput)
    elif (leagueInput.lower() == 'various'):
        parseVariousSportsCSVFile(connection, csvFile, delimeterInput)


if __name__ == "__main__":
    main()
