__author__ = '3buson'


def getAllMatches(connection, leagueId, seasonIds='all', competitionStage='all'):
    cursor = connection.cursor()

    if leagueId is None:
        return 'Please choose a leagueId!'

    if seasonIds == 'all':
        if competitionStage == 'all':
            cursor.execute('''
                            SELECT
                                m.season_id, m.date, m.home_club_id, m.away_club_id,
                                m.home_score, m.away_score, m.home_odds, m.away_odds,
                                m.home_odds_prog, m.away_odds_prog, m.extra_time,
                                hc.name, ac.name
                            FROM
                                matches m
                            JOIN
                                clubs hc
                            ON
                                hc.id = m.home_club_id
                            JOIN
                                clubs ac
                            ON
                                ac.id = m.away_club_id
                            WHERE
                                m.leagueId = %s
                            ''' %
                            leagueId)
        else:
            cursor.execute('''
                            SELECT
                                m.season_id, m.date, m.home_club_id, m.away_club_id,
                                m.home_score, m.away_score, m.home_odds, m.away_odds,
                                m.home_odds_prog, m.away_odds_prog, m.extra_time,
                                hc.name, ac.name
                            FROM
                                matches m
                            JOIN
                                clubs hc
                            ON
                                hc.id = m.home_club_id
                            JOIN
                                clubs ac
                            ON
                                ac.id = m.away_club_id
                            WHERE
                                m.leagueId = %s
                            AND
                                m.stage = "%s"
                            ''' %
                           (leagueId, competitionStage))
    else:
        if competitionStage == 'all':
            cursor.execute('''
                            SELECT
                                m.season_id, m.date, m.home_club_id, m.away_club_id,
                                m.home_score, m.away_score, m.home_odds, m.away_odds,
                                m.home_odds_prog, m.away_odds_prog, m.extra_time,
                                hc.name, ac.name
                            FROM
                                matches m
                            JOIN
                                clubs hc
                            ON
                                hc.id = m.home_club_id
                            JOIN
                                clubs ac
                            ON
                                ac.id = m.away_club_id
                            WHERE
                                m.league_id = %s
                            AND
                                m.season_id IN (%s)
                            ''' %
                           (leagueId, seasonIds))
        else:
            cursor.execute('''
                            SELECT
                                m.season_id, m.date, m.home_club_id, m.away_club_id,
                                m.home_score, m.away_score, m.home_odds, m.away_odds,
                                m.home_odds_prog, m.away_odds_prog, m.extra_time,
                                hc.name, ac.name
                            FROM
                                matches m
                            JOIN
                                clubs hc
                            ON
                                hc.id = m.home_club_id
                            JOIN
                                clubs ac
                            ON
                                ac.id = m.away_club_id
                            WHERE
                                m.league_id = %s
                            AND
                                m.season_id IN (%s)
                            AND
                                m.stage = "%s"
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
