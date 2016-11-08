__author__ = '3buson'

import databaseBridger

import sys
import math
import networkx as nx

sys.path.insert(0, '../')
import utils

def calculateEdgeWeight(winnerScore, loserScore, extraTime):
    if (extraTime):
        return 0.1
    else:
        return 0.1 + math.log(max(1, float(winnerScore - loserScore) * 100 / (loserScore)))

    # if (extraTime):
    #     return 1
    # else:
    #     return winnerScore - loserScore

def buildNetwork(leagueId, seasonId, directed=True, weighted=True):
    print "\n[Network Builder]  Creating network for leagueId %d, seasonId %d..." % (leagueId, seasonId)
    print "[Network Builder]  Network properties: directed=%d, weighted=%d" % (directed, weighted)

    connection = utils.connectToDB()

    if(directed):
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    matchesData = databaseBridger.getAllMatches(connection, leagueId, seasonId)

    for matchRecord in matchesData:
        homeClub = matchRecord[2]
        awayClub = matchRecord[3]

        homeScore = matchRecord[4]
        awayScore = matchRecord[5]

        extraTime = matchRecord[10]

        weight = 1

        if (homeScore > awayScore):
            if (weighted):
                weight = calculateEdgeWeight(homeScore, awayScore, bool(extraTime))

            graph.add_edge(int(homeClub), int(awayClub), weight=weight)
        else:
            if (weighted):
                weight = calculateEdgeWeight(awayScore, homeScore, bool(extraTime))

            graph.add_edge(int(awayClub), int(homeClub), weight=weight)

    return graph
