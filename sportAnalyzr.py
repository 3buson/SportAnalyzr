import os
import sys
import time

import utils
import databaseBridger

from NetworkManipulator import networkAnalyzr


__author__ = '3buson'


def main():
    connection = utils.connectToDB()

    leaguesInput  = raw_input('Please enter desired league ids separated by comma (all for all of them): ')
    seasonsInput  = raw_input('Please enter desired seasons separated by comma (all for all of them): ')
    directedInput = raw_input('Do you want to analyze a directed network? (0/1): ')
    weightedInput = raw_input('Do you want to analyze a weighted network? (0/1): ')

    if leaguesInput.lower() == 'all':
        leagues = databaseBridger.getAllLeagues(connection)
        leagues = list(map(lambda league: league[0], leagues))
    else:
        leagues = leaguesInput.rstrip(',').split(',')
        leagues = [int(league) for league in leagues]

    if bool(int(weightedInput)):
        logWeightsInput = raw_input('Do you want to calculate weights with logarithmic function? (0/1): ')
    else:
        logWeightsInput = 0

    analyzeBySeasonInput = raw_input('Do you want to analyze network properties season by season? (0/1): ')
    analyzeOverTimeInput = raw_input('Do you want to analyze properties over time? (0/1): ')

    isDirected      = bool(int(directedInput))
    isWeighted      = bool(int(weightedInput))
    hasLogWeights   = bool(int(logWeightsInput))
    analyzeOverTime = bool(int(analyzeOverTimeInput))
    analyzeBySeason = bool(int(analyzeBySeasonInput))

    if analyzeBySeason:
        printToFileInput = raw_input('Do you want to have output in a file? (0/1): ')
        printToFile      = bool(int(printToFileInput))
    else:
        printToFile = False

    csvOutputInput = raw_input('Do you want to have basic output in a CSV? (0/1): ')
    printToCsv     = bool(int(csvOutputInput))

    timeStartInitial = time.time()
    for leagueId in leagues:
        timeStart = time.time()

        file               = None
        leagueString       = databaseBridger.getLeagueNameFromId(connection, leagueId)
        outputFolderPrefix = 'output/' + leagueString + '/'
        outputFileSuffix   = ''

        print "\n[Network Analyzr]  Analyzing league %s..." % leagueString

        if not os.path.exists(outputFolderPrefix):
            os.makedirs(outputFolderPrefix)

        if printToFile:
            outputFileBaseName = 'networkStats'

            if isDirected:
                outputFileSuffix += '_directed'
            if isWeighted:
                outputFileSuffix += '_weighted'

            if printToCsv:
                file = open(outputFolderPrefix + outputFileBaseName + outputFileSuffix + '.csv', 'w')
            else:
                file = open(outputFolderPrefix + outputFileBaseName + outputFileSuffix + '.txt', 'w')
                sys.stdout = file

        if seasonsInput.lower() == 'all':
            seasons = databaseBridger.getAllSeasonsForLeague(connection, leagueId)
            seasons = list(map(lambda season: season[0], seasons))
        else:
            seasons = seasonsInput.rstrip(',').split(',')
            seasons = [int(season) for season in seasons]

        competitionStages = databaseBridger.getAllCompetitionStagesForLeague(connection, leagueId)
        competitionStages = list(map(lambda stage: stage[0], competitionStages))


        if analyzeBySeason:
            index = 0
            for seasonId in seasons:
                print "\n[Network Analyzr]  Analyzing season %s..." % seasonId

                for competitionStage in competitionStages:
                    networkAnalyzr.createAndAnalyzeNetwork(leagueId, leagueString, seasonId, competitionStage, isDirected, isWeighted, hasLogWeights, file, printToCsv, not bool(index))

                if len(competitionStages) > 1:
                    networkAnalyzr.createAndAnalyzeNetwork(leagueId, leagueString, seasonId, 'all', isDirected, isWeighted, hasLogWeights, file, printToCsv, not bool(index))

                index += 1

                print ''

        if analyzeOverTime:
            print "\n[Network Analyzr]  Building networks for all seasons"

            for competitionStage in competitionStages:
                networkAnalyzr.createAndAnalyzeNetworksOverTime(leagueId, leagueString, seasons, competitionStage, isDirected, isWeighted, hasLogWeights)

            if len(competitionStages) > 1:
                networkAnalyzr.createAndAnalyzeNetworksOverTime(leagueId, leagueString, seasons, 'all', isDirected, isWeighted, hasLogWeights)

        timeSpent = time.time() - timeStart
        timeStart = time.time()

        print "\n[Network Analyzr]  Analysis of league '%s' done, time spent: %d s" % (leagueString, int(round(timeSpent)))

    totalTimeSpent = time.time() - timeStartInitial

    print "\n[Network Analyzr]  Analysis done, total time spent: %d s" % int(round(totalTimeSpent))

    return 0


if __name__ == "__main__":
    main()