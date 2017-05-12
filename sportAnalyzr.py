import os
import sys
import csv
import time

from random import shuffle

import utils
import constants
import databaseBridger

from NetworkManipulator import networkAnalyzr
from Visualizer import visualizer

__author__ = '3buson'


def analyze(connection, leagues, seasonsInput, isDirected, isWeighted, analyzeBySeason, analyzeOverTime, hasLogWeights, hasSimpleWeights, printToFile, printToCsv, colors):
    timeStartInitial = time.time()

    for leagueId in leagues:
        timeStart = time.time()

        file = None
        leagueString = databaseBridger.getLeagueNameFromId(connection, leagueId)
        outputFolderPrefix = 'output/' + leagueString + '/'
        outputFileSuffix = ''

        if leagueString is 'National Basketball Association':
            hasSimpleWeights = False

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
                    networkAnalyzr.createAndAnalyzeNetwork(leagueId, leagueString, seasonId, competitionStage,
                                                           isDirected, isWeighted, hasLogWeights, file, printToCsv,
                                                           not bool(index))

                if len(competitionStages) > 1:
                    networkAnalyzr.createAndAnalyzeNetwork(leagueId, leagueString, seasonId, 'all', isDirected,
                                                           isWeighted, hasLogWeights, file, printToCsv, not bool(index))

                index += 1

                print ''

        if analyzeOverTime:
            print "\n[Network Analyzr]  Building networks for all seasons"

            for competitionStage in competitionStages:
                networkAnalyzr.createAndAnalyzeNetworksOverTime(leagueId, leagueString, seasons, competitionStage,
                                                                isDirected, isWeighted, hasSimpleWeights, hasLogWeights)

            if len(competitionStages) > 1:
                networkAnalyzr.createAndAnalyzeNetworksOverTime(leagueId, leagueString, seasons, 'all', isDirected,
                                                                isWeighted, hasSimpleWeights, hasLogWeights)

        timeSpent = time.time() - timeStart
        timeStart = time.time()

        print "\n[Network Analyzr]  Analysis of league '%s' done, time spent: %d s" % (
        leagueString, int(round(timeSpent)))
        print "____________________________________________________________________________________________________\n\n"

    # draw combined relative entropy graphs
    if len(leagues) > 1 and analyzeOverTime:
        seasonsDoubleArray = list()
        relativeEntropies = list()
        leagueStrings = list()

        for leagueId in leagues:
            leagueString = databaseBridger.getLeagueNameFromId(connection, leagueId)
            filename = 'output/' + leagueString + 'NetworkPropertiesOverTimeRegular' + '.csv'

            with open(filename, 'rb') as f:
                reader = csv.reader(f, delimiter=',')

                leagueRelativeEntropyList = list()

                for row in reader:
                    if row[0] == 'pageRankRelativeEntropy' and row[2] == 'regular' and row[3] == '0.85':
                        seasonsForLeague = row[4].split(' ')
                        leagueRelativeEntropyList = row[5].split(' ')

                        break

            seasonsDoubleArray.append(seasonsForLeague)
            relativeEntropies.append(leagueRelativeEntropyList)
            leagueStrings.append(leagueString)

        relativeEntropyGraphFilename = 'output/pageRank_over_time_multi_leagues_relative_entropy'

        visualizer.createMultiGraph(None, None, False, 'Relative PR Entropy of Leagues Over Time', 'Season',
                                    'Relative PageRank Entropy', relativeEntropyGraphFilename, seasonsDoubleArray,
                                    relativeEntropies, colors, leagueStrings)

    totalTimeSpent = time.time() - timeStartInitial

    print "\n[Network Analyzr]  Analysis done, total time spent: %d s" % int(round(totalTimeSpent))


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
        simpleWeightsInput = raw_input('Do you want to have weights only by score? (0/1): ')

        if bool(int(simpleWeightsInput)):
            logWeightsInput = 0
        else:
            logWeightsInput = raw_input('Do you want to calculate weights with logarithmic function? (0/1): ')
    else:
        logWeightsInput = 0

    analyzeBySeasonInput = raw_input('Do you want to analyze network properties season by season? (0/1): ')
    analyzeOverTimeInput = raw_input('Do you want to analyze properties over time? (0/1): ')

    isDirected       = bool(int(directedInput))
    isWeighted       = bool(int(weightedInput))
    hasSimpleWeights = bool(int(simpleWeightsInput))
    hasLogWeights    = bool(int(logWeightsInput))
    analyzeOverTime  = bool(int(analyzeOverTimeInput))
    analyzeBySeason  = bool(int(analyzeBySeasonInput))

    if analyzeBySeason:
        printToFileInput = raw_input('Do you want to have output in a file? (0/1): ')
        printToFile      = bool(int(printToFileInput))
    else:
        printToFile = False

    csvOutputInput = raw_input('Do you want to have basic network stats output in a CSV? (0/1): ')
    printToCsv     = bool(int(csvOutputInput))

    # 26 RGB colors for relative entropy graph
    colors = constants.rgb26
    # mix them so similar colors will not get plotted together
    shuffle(colors)

    # scale RGB values to the [0, 1] interval
    for i in range(len(colors)):
        r, g, b = colors[i]
        colors[i] = (r / 255.0, g / 255.0, b / 255.0)

    analyze(connection, leagues, seasonsInput, isDirected, isWeighted, analyzeBySeason, analyzeOverTime, hasLogWeights, hasSimpleWeights, printToFile, printToCsv, colors)

    return 0


if __name__ == "__main__":
    main()
