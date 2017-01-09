__author__ = '3buson'

import databaseBridger

import sys
import math
import networkx as nx

sys.path.insert(0, '../')
import utils


def calculateEdgeWeight(winnerScore, loserScore, extraTime, logarithmic=False, penalizeExtraTime=False):
    if extraTime and penalizeExtraTime:
        weight = 1.0 / winnerScore
    else:
        weight = float(winnerScore - loserScore) / (winnerScore)

    if logarithmic:
        weight = math.log(1 + weight)

    return weight * 10


def buildNetwork(leagueId, seasonId, competitionStage, directed=True, weighted=True, logWeights=False):
    print "\n[Network Builder]  Creating network for leagueId %d, seasonId %d, competition stage %s..." %\
          (leagueId, seasonId, competitionStage)
    print "[Network Builder]  Network properties: directed=%d, weighted=%d" % (directed, weighted)

    connection = utils.connectToDB()

    if directed:
        graph = nx.MultiDiGraph()
    else:
        graph = nx.MultiGraph()

    matchesData = databaseBridger.getAllMatches(connection, leagueId, seasonId, competitionStage)

    for matchRecord in matchesData:
        homeClub = matchRecord[2]
        awayClub = matchRecord[3]

        homeScore = matchRecord[4]
        awayScore = matchRecord[5]

        extraTime = matchRecord[10]

        weight = 1

        if homeScore > awayScore:
            if weighted:
                weight = calculateEdgeWeight(homeScore, awayScore, bool(extraTime), logWeights)

            graph.add_edge(int(awayClub), int(homeClub), weight=weight)
        else:
            if weighted:
                weight = calculateEdgeWeight(awayScore, homeScore, bool(extraTime), logWeights)

            graph.add_edge(int(homeClub), int(awayClub), weight=weight)

    return graph
