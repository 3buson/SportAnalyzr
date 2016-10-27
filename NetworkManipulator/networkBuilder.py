__author__ = '3buson'

import databaseBridger

import sys

sys.path.insert(0, '../')
import utils

def buildNetwork(leagueId, seasonId):
    connection = utils.connectToDB()

    matchesData = databaseBridger.getAllMatches(connection, leagueId, seasonId)

    for matchRecord in matchesData:
        # TODO: build clubs network

    return ''