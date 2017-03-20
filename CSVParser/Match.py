import pyodbc
import traceback


__author__ = '3buson'


class Match:

    def __init__(self, seasonId=None, leagueId=None, date=None, stage=None,
                 homeClubId=None, awayClubId=None, homeScore=None, awayScore=None,
                 homeOdds=None, awayOdds=None, homeOddsProg=None, awayOddsProg=None, extraTime=None):
        self.id           = id
        self.seasonId     = seasonId
        self.leagueId     = leagueId
        self.date         = date
        self.stage        = stage
        self.homeClubId   = homeClubId
        self.awayClubId   = awayClubId
        self.homeScore    = homeScore
        self.awayScore    = awayScore
        self.homeOdds     = homeOdds
        self.awayOdds     = awayOdds
        self.homeOddsProg = homeOddsProg
        self.awayOddsProg = awayOddsProg
        self.extraTime    = extraTime

    def dbInsert(self, connection):
        cursor = connection.cursor()

        try:
            cursor.execute('''
                            INSERT IGNORE INTO matches(season_id, league_id, date, stage,
                                                        home_club_id, away_club_id, home_score, away_score,
                                                        home_odds, away_odds, home_odds_prog, away_odds_prog, extra_time)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                           ''',
                           self.seasonId, self.leagueId, self.date, self.stage,
                           self.homeClubId, self.awayClubId, self.homeScore, self.awayScore,
                           self.homeOdds, self.awayOdds, self.homeOddsProg, self.awayOddsProg,
                           self.extraTime)

        except pyodbc.DatabaseError, e:
            print "[Club class]  ERROR - DatabaseError", e
            traceback.print_exc()

        connection.commit()
