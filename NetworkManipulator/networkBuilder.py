import math

import networkx as nx

import utils
import databaseBridger


__author__ = '3buson'


def calculateEdgeWeight(winnerScore, loserScore, extraTime, logarithmic=False, penalizeExtraTime=False):
    # improved weights
    if winnerScore > 15:
        alpha = 1
    else:
        alpha = 2

    if winnerScore == 0 and loserScore == 0:
        weight = 0
    else:
        weight = alpha * ((loserScore - winnerScore) / (winnerScore + loserScore))

    return 1 / (1 + math.exp(-weight))

    # if extraTime and penalizeExtraTime:
    #     weight = 1.0 / winnerScore
    # else:
    #     weight = float(winnerScore - loserScore) / (max(1, winnerScore))
    #
    # if logarithmic:
    #     weight = math.log(1 + weight)
    #
    # return weight * 10


def buildNetwork(leagueId, seasonId, competitionStage, directed=True, weighted=True, simpleWeights=False, logWeights=False):
    print "[Network Builder]  Creating network for leagueId %d, seasonId %d, competition stage %s..." %\
          (leagueId, seasonId, competitionStage)

    if utils.mode == 'debug':
        print "[Network Builder]  Network properties: directed=%d, weighted=%d" % (directed, weighted)

    connection = utils.connectToDB()

    if directed:
        graph = nx.MultiDiGraph()
    else:
        graph = nx.MultiGraph()

    matchesData = databaseBridger.getAllMatches(connection, leagueId, seasonId, competitionStage)

    for matchRecord in matchesData:
        homeClub = int(matchRecord[2])
        awayClub = int(matchRecord[3])

        homeClubName = matchRecord[11]
        awayClubName = matchRecord[12]

        homeScore = matchRecord[4]
        awayScore = matchRecord[5]

        extraTime = matchRecord[10]

        weight = 1

        if not graph.has_node(homeClub):
            graph.add_node(homeClub, name=homeClubName)

        if not graph.has_node(awayClub):
            graph.add_node(awayClub, name=awayClubName)

        # if simpleWeights:
        #     if homeScore:
        #         graph.add_edge(awayClub, homeClub, weight=homeScore)
        #     if awayScore:
        #         graph.add_edge(homeClub, awayClub, weight=awayScore)
        # else:
        #     if homeScore > awayScore:
        #         if weighted:
        #             weight = calculateEdgeWeight(homeScore, awayScore, bool(extraTime), logWeights)
        #
        #         graph.add_edge(awayClub, homeClub, weight=weight)
        #     else:
        #         if weighted:
        #             weight = calculateEdgeWeight(awayScore, homeScore, bool(extraTime), logWeights)
        #
        #         graph.add_edge(homeClub, awayClub, weight=weight)

        # improved weights
        weight = calculateEdgeWeight(homeScore, awayScore, bool(extraTime), logWeights)
        graph.add_edge(awayClub, homeClub, weight=weight)

        weight = calculateEdgeWeight(awayScore, homeScore, bool(extraTime), logWeights)
        graph.add_edge(homeClub, awayClub, weight=weight)

    return graph
