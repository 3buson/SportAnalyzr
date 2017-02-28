__author__ = '3buson'

import sys

sys.path.insert(0, '../')

def getAllMatches(connection, leagueId, seasonIds='all', competitionStage='all'):
    cursor = connection.cursor()

    if leagueId is None:
        return 'Please choose a leagueId!'

    if seasonIds == 'all':
        if competitionStage == 'all':
            cursor.execute('''
                            SELECT
                                seasonId, date, home_club_id, away_club_id,
                                home_score, away_score, home_odds, away_odds,
                                home_odds_prog, away_odds_prog, extra_time
                            FROM
                                matches
                            WHERE
                                leagueId = %s
                            ''' %
                            leagueId)
        else:
            cursor.execute('''
                            SELECT
                                seasonId, date, home_club_id, away_club_id,
                                home_score, away_score, home_odds, away_odds,
                                home_odds_prog, away_odds_prog, extra_time
                            FROM
                                matches
                            WHERE
                                leagueId = %s
                            AND
                                stage = "%s"
                            ''' %
                           (leagueId, competitionStage))
    else:
        if competitionStage == 'all':
            cursor.execute('''
                            SELECT
                                season_id, date, home_club_id, away_club_id,
                                home_score, away_score, home_odds, away_odds,
                                home_odds_prog, away_odds_prog, extra_time
                            FROM
                                matches
                            WHERE
                                league_id = %s
                            AND
                                season_id IN (%s)
                            ''' %
                           (leagueId, seasonIds))
        else:
            cursor.execute('''
                            SELECT
                                season_id, date, home_club_id, away_club_id,
                                home_score, away_score, home_odds, away_odds,
                                home_odds_prog, away_odds_prog, extra_time
                            FROM
                                matches
                            WHERE
                                league_id = %s
                            AND
                                season_id IN (%s)
                            AND
                                stage = "%s"
                            ''' %
                           (leagueId, seasonIds, competitionStage))

    return cursor.fetchall()

def getAllClubsForLeague(connection, leagueId):
    cursor = connection.cursor()

    if leagueId is None:
        return 'Please choose a leagueId!'

    cursor.execute('''
                        SELECT
                            id, acronym, name
                        FROM
                            clubs
                        WHERE
                            league_id = %s
                        ''' %
                    leagueId)

    return cursor.fetchall()

def getAllLeagues(connection):
    cursor = connection.cursor()

    cursor.execute('''
                    SELECT
                        id
                    FROM
                        leagues
                    ''')

    return cursor.fetchall()


def getAllSeasonsForLeague(connection, leagueId):
    cursor = connection.cursor()

    if leagueId is None:
        return 'Please choose a leagueId!'

    cursor.execute('''
                        SELECT
                            DISTINCT (season_id)
                        FROM
                            matches
                        WHERE
                            league_id = %s
                        ''' %
                   leagueId)

    return cursor.fetchall()

def getAllCompetitionStagesForLeague(connection, leagueId):
    cursor = connection.cursor()

    if leagueId is None:
        return 'Please choose a leagueId!'

    cursor.execute('''
                        SELECT
                            DISTINCT (stage)
                        FROM
                            matches
                        WHERE
                            league_id = %s
                        ''' %
                   leagueId)

    return cursor.fetchall()

def getLeagueNameFromId(connection, leagueId):
    cursor = connection.cursor()

    if leagueId is None:
        return 'Please choose a leagueId!'

    cursor.execute('''
                            SELECT
                                name
                            FROM
                                leagues
                            WHERE
                                id = %s
                            ''' %
                   leagueId)

    return cursor.fetchone()[0]
