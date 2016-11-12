__author__ = '3buson'

import sys

sys.path.insert(0, '../')

def getAllMatches(connection, leagueId, seasonIds='all', competitionStage='all'):
    cursor = connection.cursor()

    if (leagueId == None):
        return 'Please choose a leagueId!'

    if (seasonIds == 'all'):
        if (competitionStage == 'all'):
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
                                stage = '%s'
                            ''' %
                           (leagueId, competitionStage))
    else:
        if (competitionStage == 'all'):
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
                                stage = '%s'
                            ''' %
                           (leagueId, seasonIds, competitionStage))

    return cursor.fetchall()

def getAllClubs(connection, leagueId):
    cursor = connection.cursor

    if (leagueId == None):
        return 'Please choose a leagueId!'

    cursor.execute('''
                    SELECT
                        id, acronym, name
                    FROM
                        clubs
                    WHERE
                        leagueId = %s
                    ''' %
                    leagueId)

    return cursor.fetchAll()
