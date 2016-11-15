__author__ = '3buson'

import databaseBridger

import sys
import networkx as nx

sys.path.insert(0, '../')
import utils


def calculateEdgeWeight(winnerScore, loserScore, extraTime, penalizeExtraTime=False):
    if (extraTime and penalizeExtraTime):
        return 1.0 / winnerScore
    else:
        return float(winnerScore - loserScore) / (winnerScore)

    # if (extraTime):
    #     return 1
    # else:
    #     return winnerScore - loserScore


def buildNetwork(leagueId, seasonId, competitionStage, directed=True, weighted=True):
    print "\n[Network Builder]  Creating network for leagueId %d, seasonId %d, competition stage %s..." %\
          (leagueId, seasonId, competitionStage)
    print "[Network Builder]  Network properties: directed=%d, weighted=%d" % (directed, weighted)

    connection = utils.connectToDB()

    if(directed):
        graph = nx.DiGraph()
    else:
        graph = nx.Graph()

    matchesData = databaseBridger.getAllMatches(connection, leagueId, seasonId, competitionStage)

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

            graph.add_edge(int(awayClub), int(homeClub), weight=weight)
        else:
            if (weighted):
                weight = calculateEdgeWeight(awayScore, homeScore, bool(extraTime))

            graph.add_edge(int(homeClub), int(awayClub), weight=weight)

    return graph
