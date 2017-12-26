import math
import numpy

import utils
import databaseBridger


__author__ = '3buson'


def buildGamesMatrix(games, numTeams):
    M = numpy.zeros([len(games), numTeams])
    row = 0

    for g in games:
        M[row, g[0]] = 1
        M[row, g[1]] = -1
        row += 1

    return M


def buildOutcomes(games):
    E = numpy.zeros([len(games)])
    row = 0

    for g in games:
        E[row] = g[2]
        row += 1

    return E


def calculateMasseyRatings(leagueId, seasonId):
    connection = utils.connectToDB()
    matchesData = databaseBridger.getAllMatches(connection, leagueId, seasonId, 'regular')
    clubsDict = dict()
    numClubs = 0
    games = []

    for matchRecord in matchesData:
        homeClub = int(matchRecord[2])
        awayClub = int(matchRecord[3])

        # reindex club ids
        if homeClub in clubsDict:
            homeClubReindexed = clubsDict[homeClub]
        else:
            homeClubReindexed = numClubs
            numClubs = numClubs + 1
            clubsDict[homeClub] = homeClubReindexed

        if awayClub in clubsDict:
            awayClubReindexed = clubsDict[awayClub]
        else:
            awayClubReindexed = numClubs
            numClubs = numClubs + 1
            clubsDict[awayClub] = awayClubReindexed

        homeScore = matchRecord[4]
        awayScore = matchRecord[5]

        games.append([homeClubReindexed, awayClubReindexed, homeScore - awayScore])

    numClubs = len(clubsDict)

    M = buildGamesMatrix(games, numClubs)
    E = buildOutcomes(games)
    M = numpy.vstack((M, numpy.ones([numClubs])))
    E = numpy.append(E, 0)

    ratings = numpy.linalg.lstsq(M, E)[0]

    return ratings, numClubs


def calculateRelativeMasseyEntropy(leagueId, seasonId):
    print "[Massey Analyzr]  Calculating Massey ratings for league %d and season %s" % (leagueId, seasonId)

    ratings, numClubs = calculateMasseyRatings(leagueId, seasonId)

    if utils.mode == 'debug':
        print "[Massey Analyzr]  Massey ratings calculated:\n"
        print ratings
        print "\n"

    # transform Massey ratings to [0,1] interval
    scale = (max(ratings) - min(ratings)) / (1 - 0)
    translation = min(ratings) - 0.0000000001
    ratingsTranslated = [x - translation for x in ratings]
    ratingsScaled = [x / scale for x in ratingsTranslated]

    # entropy of Massey ratings
    entropy = 0
    masseySum = sum(ratingsScaled)
    for masseyRating in ratingsScaled:
        p = masseyRating / masseySum

        if p > 0:
            entropy += p * math.log(p, 2)
        else:
            print "[Massey Analyzr]  Entropy is ZERO!"

    entropy = -entropy
    relativeEntropy = entropy / math.log(numClubs, 2)

    print "[Massey Analyzr]  Relative entropy of Massey ratings: ", relativeEntropy

    return relativeEntropy
