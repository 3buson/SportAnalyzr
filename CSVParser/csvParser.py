import os
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


def parseBetsCSVFile(csvsFolder, delimiter):
    filenum = 0
    numFiles = len(os.listdir(csvsFolder))
    betsDict = dict()

    for csvFile in os.listdir(csvsFolder):
        filenum += 1

        print "\n[CSV Parser]  Parsing file %d/%d with filename %s" % (filenum, numFiles, csvFile)

        rownum = 0
        with open(csvsFolder + csvFile, 'rb') as f:
            reader = csv.reader(f, delimiter=delimiter)

            for row in reader:
                # skip header
                if rownum == 0:
                    rownum += 1
                else:
                    betType = row[5].strip()

                    if (betType == 'Match Odds'):
                        leagueString = row[3].strip()

                        season_string = str(row[2])

                        season_array = season_string.split('-')

                        if len(season_array) < 2:
                            continue

                        month = int(season_array[1])
                        year = season_string.split('-')[2].split(' ')[0]

                        if month < 7:
                            season = str(int(year) - 1)

                        if 'Barclays Premiership' in leagueString or 'Barclays Premier League' in leagueString:
                            if 'ENG' not in betsDict.keys():
                                betsDict['ENG'] = dict()

                            if season in betsDict['ENG'].keys():
                                betsDict['ENG'][season] += float(row[11])
                            else:
                                betsDict['ENG'][season] = float(row[11])
                        if 'Spanish Soccer/Primera Division' in leagueString:
                            if 'ESP' not in betsDict.keys():
                                betsDict['ESP'] = dict()

                            if season in betsDict['ESP'].keys():
                                betsDict['ESP'][season] += float(row[11])
                            else:
                                betsDict['ESP'][season] = float(row[11])
                        if 'Bundesliga/' in leagueString:
                            if 'GER' not in betsDict.keys():
                                betsDict['GER'] = dict()

                            if season in betsDict['GER'].keys():
                                betsDict['GER'][season] += float(row[11])
                            else:
                                betsDict['GER'][season] = float(row[11])
                        if 'Serie A' in leagueString:
                            if 'ITA' not in betsDict.keys():
                                betsDict['ITA'] = dict()

                            if season in betsDict['ITA'].keys():
                                betsDict['ITA'][season] += float(row[11])
                            else:
                                betsDict['ITA'][season] = float(row[11])
                        if 'Ligue 1 Orange' in leagueString:
                            if 'FRA' not in betsDict.keys():
                                betsDict['FRA'] = dict()

                            if season in betsDict['FRA'].keys():
                                betsDict['FRA'][season] += float(row[11])
                            else:
                                betsDict['FRA'][season] = float(row[11])
                        if 'Dutch Soccer/Eredivisie' in leagueString:
                            if 'NED' not in betsDict.keys():
                                betsDict['NED'] = dict()

                            if season in betsDict['NED'].keys():
                                betsDict['NED'][season] += float(row[11])
                            else:
                                betsDict['NED'][season] = float(row[11])
                        if 'Belgian Soccer/Jupiler League' in leagueString or 'Belgian Soccer/Belgian Jupiler League' in leagueString:
                            if 'BEL' not in betsDict.keys():
                                betsDict['BEL'] = dict()

                            if season in betsDict['BEL'].keys():
                                betsDict['BEL'][season] += float(row[11])
                            else:
                                betsDict['BEL'][season] = float(row[11])
                        if 'Turkish Soccer/Super League' in leagueString or 'Turkish Soccer/Turkish Super League' in leagueString:
                            if 'TUR' not in betsDict.keys():
                                betsDict['TUR'] = dict()

                            if season in betsDict['TUR'].keys():
                                betsDict['TUR'][season] += float(row[11])
                            else:
                                betsDict['TUR'][season] = float(row[11])
                        if 'Greek Soccer/National Liga' in leagueString or 'Greek Soccer/Greek Super League' in leagueString:
                            if 'GRE' not in betsDict.keys():
                                betsDict['GRE'] = dict()

                            if season in betsDict['GRE'].keys():
                                betsDict['GRE'][season] += float(row[11])
                            else:
                                betsDict['GRE'][season] = float(row[11])
                        if 'Scottish Soccer/Scottish Premiership' in leagueString or 'Scottish Soccer/Bank of Scot Prem' in leagueString:
                            if 'SCO' not in betsDict.keys():
                                betsDict['SCO'] = dict()

                            if season in betsDict['SCO'].keys():
                                betsDict['SCO'][season] += float(row[11])
                            else:
                                betsDict['SCO'][season] = float(row[11])
                        if 'NBA' in leagueString:
                            if 'NBA' not in betsDict.keys():
                                betsDict['NBA'] = dict()

                            if season in betsDict['NBA'].keys():
                                betsDict['NBA'][season] += float(row[11])
                            else:
                                betsDict['NBA'][season] = float(row[11])

    for league, seasonsDict in betsDict.iteritems():
        print "\n[CSV Parser]  Bets volume for league %s" % league
        for season, volume in seasonsDict.iteritems():
            print "%s,%d" % (season, int(volume))


def parseBetsCSVFileByGame(csvsFolder, delimiter):
    filenum = 0
    numFiles = len(os.listdir(csvsFolder))
    oddsDict = dict()
    uniformityDict = dict()

    for csvFile in os.listdir(csvsFolder):
        filenum += 1

        print "\n[CSV Parser]  Parsing file %d/%d with filename %s" % (filenum, numFiles, csvFile)

        rownum = 0
        with open(csvsFolder + csvFile, 'rb') as f:
            reader = csv.reader(f, delimiter=delimiter)

            for row in reader:
                # skip header
                if rownum == 0:
                    rownum += 1
                else:
                    betType = row[5].strip()

                    if (betType == 'Match Odds'):
                        eventId = row[1]
                        leagueString = row[3].strip()
                        odds = float(row[9])
                        volumeMatched = float(row[11])

                        if 'Barclays Premiership' in leagueString or 'Barclays Premier League' in leagueString:
                            if 'ENG' not in oddsDict.keys():
                                oddsDict['ENG'] = dict()
                                uniformityDict['ENG'] = dict()

                            if eventId not in oddsDict['ENG'].keys():
                                oddsDict['ENG'][eventId] = dict()
                            else:
                                if not odds in oddsDict['ENG'][eventId].keys():
                                    oddsDict['ENG'][eventId][odds] = volumeMatched
                                else:
                                    oddsDict['ENG'][eventId][odds] += volumeMatched
                        if 'Spanish Soccer/Primera Division' in leagueString:
                            if 'ESP' not in oddsDict.keys():
                                oddsDict['ESP'] = dict()
                                uniformityDict['ESP'] = dict()

                            if eventId not in oddsDict['ESP'].keys():
                                oddsDict['ESP'][eventId] = dict()
                            else:
                                if not odds in oddsDict['ESP'][eventId].keys():
                                    oddsDict['ESP'][eventId][odds] = volumeMatched
                                else:
                                    oddsDict['ESP'][eventId][odds] += volumeMatched
                        if 'Bundesliga/' in leagueString:
                            if 'GER' not in oddsDict.keys():
                                oddsDict['GER'] = dict()
                                uniformityDict['GER'] = dict()

                            if eventId not in oddsDict['GER'].keys():
                                oddsDict['GER'][eventId] = dict()
                            else:
                                if not odds in oddsDict['GER'][eventId].keys():
                                    oddsDict['GER'][eventId][odds] = volumeMatched
                                else:
                                    oddsDict['GER'][eventId][odds] += volumeMatched
                        if 'Serie A' in leagueString:
                            if 'ITA' not in oddsDict.keys():
                                oddsDict['ITA'] = dict()
                                uniformityDict['ITA'] = dict()

                            if eventId not in oddsDict['ITA'].keys():
                                oddsDict['ITA'][eventId] = dict()
                            else:
                                if not odds in oddsDict['ITA'][eventId].keys():
                                    oddsDict['ITA'][eventId][odds] = volumeMatched
                                else:
                                    oddsDict['ITA'][eventId][odds] += volumeMatched
                        if 'Ligue 1 Orange' in leagueString:
                            if 'FRA' not in oddsDict.keys():
                                oddsDict['FRA'] = dict()
                                uniformityDict['FRA'] = dict()

                            if eventId not in oddsDict['FRA'].keys():
                                oddsDict['FRA'][eventId] = dict()
                            else:
                                if not odds in oddsDict['FRA'][eventId].keys():
                                    oddsDict['FRA'][eventId][odds] = volumeMatched
                                else:
                                    oddsDict['FRA'][eventId][odds] += volumeMatched
                        if 'Dutch Soccer/Eredivisie' in leagueString:
                            if 'NED' not in oddsDict.keys():
                                oddsDict['NED'] = dict()
                                uniformityDict['NED'] = dict()

                            if eventId not in oddsDict['NED'].keys():
                                oddsDict['NED'][eventId] = dict()
                            else:
                                if not odds in oddsDict['NED'][eventId].keys():
                                    oddsDict['NED'][eventId][odds] = volumeMatched
                                else:
                                    oddsDict['NED'][eventId][odds] += volumeMatched
                        if 'Belgian Soccer/Jupiler League' in leagueString or 'Belgian Soccer/Belgian Jupiler League' in leagueString:
                            if 'BEL' not in oddsDict.keys():
                                oddsDict['BEL'] = dict()
                                uniformityDict['BEL'] = dict()

                            if eventId not in oddsDict['BEL'].keys():
                                oddsDict['BEL'][eventId] = dict()
                            else:
                                if not odds in oddsDict['BEL'][eventId].keys():
                                    oddsDict['BEL'][eventId][odds] = volumeMatched
                                else:
                                    oddsDict['BEL'][eventId][odds] += volumeMatched
                        if 'Turkish Soccer/Super League' in leagueString or 'Turkish Soccer/Turkish Super League' in leagueString:
                            if 'TUR' not in oddsDict.keys():
                                oddsDict['TUR'] = dict()
                                uniformityDict['TUR'] = dict()

                            if eventId not in oddsDict['TUR'].keys():
                                oddsDict['TUR'][eventId] = dict()
                            else:
                                if not odds in oddsDict['TUR'][eventId].keys():
                                    oddsDict['TUR'][eventId][odds] = volumeMatched
                                else:
                                    oddsDict['TUR'][eventId][odds] += volumeMatched
                        if 'Greek Soccer/National Liga' in leagueString or 'Greek Soccer/Greek Super League' in leagueString:
                            if 'GRE' not in oddsDict.keys():
                                oddsDict['GRE'] = dict()
                                uniformityDict['GRE'] = dict()

                            if eventId not in oddsDict['GRE'].keys():
                                oddsDict['GRE'][eventId] = dict()
                            else:
                                if not odds in oddsDict['GRE'][eventId].keys():
                                    oddsDict['GRE'][eventId][odds] = volumeMatched
                                else:
                                    oddsDict['GRE'][eventId][odds] += volumeMatched
                        if 'Scottish Soccer/Scottish Premiership' in leagueString or 'Scottish Soccer/Bank of Scot Prem' in leagueString:
                            if 'SCO' not in oddsDict.keys():
                                oddsDict['SCO'] = dict()
                                uniformityDict['SCO'] = dict()

                            if eventId not in oddsDict['SCO'].keys():
                                oddsDict['SCO'][eventId] = dict()
                            else:
                                if not odds in oddsDict['SCO'][eventId].keys():
                                    oddsDict['SCO'][eventId][odds] = volumeMatched
                                else:
                                    oddsDict['SCO'][eventId][odds] += volumeMatched
                        if 'NBA' in leagueString:
                            if 'NBA' not in oddsDict.keys():
                                oddsDict['NBA'] = dict()
                                uniformityDict['NBA'] = dict()

                            if eventId not in oddsDict['NBA'].keys():
                                oddsDict['NBA'][eventId] = dict()
                            else:
                                if not odds in oddsDict['NBA'][eventId].keys():
                                    oddsDict['NBA'][eventId][odds] = volumeMatched
                                else:
                                    oddsDict['NBA'][eventId][odds] += volumeMatched

    file = open('FileConqueror/csv/bets/volume_uniformity_per_game.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(['league', 'uniformity', 'betsVolume'])

    for league, leagueOddsDict in oddsDict.iteritems():
        for eventId, eventDict in leagueOddsDict.iteritems():
            uniformity = 0
            totalVolumeMatched = sum(eventDict.values())

            oddsSum = 0
            # normalize odds to sum up to 1
            for odds, volumeMatched in eventDict.iteritems():
                oddsSum += odds

            for odds, volumeMatched in eventDict.iteritems():
                uniformity += float(odds/oddsSum) * float(volumeMatched) / totalVolumeMatched

            if uniformity != 0:
                uniformity = 1.0 / uniformity

                eventDict['uniformity'] = uniformity
                eventDict['betsVolume'] = totalVolumeMatched

                writer.writerow([league, uniformity, totalVolumeMatched])


def main():
    connection = utils.connectToDB()

    csvFilename = raw_input('Please enter CSV filename: ')
    csvPath     = '../FileConqueror/csv/matches/'
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
