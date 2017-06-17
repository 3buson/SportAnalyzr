import os
import csv
import math
import numpy

import constants

from scipy import stats
from operator import add
from operator import sub
from matplotlib import pyplot


__author__ = '3buson'


### --- PLOTTING FUNCTIONS --- ###

def createGraph(xs, ys, xsMin, xsMax, ysMin, ysMax, style='b-', logScale=False, title=None, xLabel=None, yLabel=None, filename=None):
    pyplot.figure(figsize=(15, 15))

    if logScale:
        pyplot.loglog(ys, style)
    else:
        pyplot.ylim([ysMin, ysMax])
        pyplot.plot(xs, ys, style)

    if xsMin is not None and xsMax is not None:
        pyplot.xlim([xsMin, xsMax])

    if title:
        pyplot.title(title)

    if xLabel:
        pyplot.xlabel(xLabel)

    if yLabel:
        pyplot.ylabel(yLabel)

    if filename:
        pyplot.savefig(filename)
    else:
        pyplot.show()

    pyplot.close()


def createMultiGraph(ysMin=None, ysMax=None, logScale=False, title=None, xLabel=None, yLabel=None, filename=None, xs=None, ysDoubleArray=None, colors=['b', 'k', 'r', 'm', 'g'], labels=None):
    pyplot.figure(figsize=(15, 15))

    for idx, ys in enumerate(ysDoubleArray):
        if len(xs) > idx and isinstance(xs[idx], list):
            xsParsed = xs[idx]
        else:
            xsParsed = xs

        if logScale:
            pyplot.loglog(xsParsed, ys, color=colors[idx])
        else:
            if labels is not None:
                label = labels[idx]
            else:
                label = None

            pyplot.plot(xsParsed, ys, color=colors[idx], label=label)

    pyplot.legend(loc='best', prop={'size': 11})

    if title:
        pyplot.title(title)

    if xLabel:
        pyplot.xlabel(xLabel)

    if yLabel:
        pyplot.ylabel(yLabel)

    if filename:
        pyplot.savefig(filename)
    else:
        pyplot.show()

    pyplot.close()


def createDoubleGraphWithVariance(ysMin=None, ysMax=None, title=None, xLabel=None, yLabel=None, filename=None, xs=None, ys1=None, ys2=None, ys1Deviation=None, ys2Deviation=None, labels=None):
    pyplot.figure(figsize=(15, 15))

    if ysMin is not None and ysMax is not None:
        pyplot.ylim([ysMin, ysMax])

    if ys1:
        if labels is not None:
            label = labels[0]
        else:
            label = None

        pyplot.plot(xs, ys1, 'b-', label=label)

    if ys1Deviation:
        deviationUp   = map(add, ys1, ys1Deviation)
        deviationDown = map(sub, ys1, ys1Deviation)

        pyplot.plot(xs, deviationUp,   'b--')
        pyplot.plot(xs, deviationDown, 'b--')

    if ys2:
        if labels is not None:
            label = labels[0]
        else:
            label = None

        pyplot.plot(xs, ys2, 'r-', label=label)

    if ys2Deviation:
        deviationUp   = map(add, ys2, ys2Deviation)
        deviationDown = map(sub, ys2, ys2Deviation)

        pyplot.plot(xs, deviationUp,   'r--')
        pyplot.plot(xs, deviationDown, 'r--')

    pyplot.legend(loc='best', prop={'size': 11})

    if title:
        pyplot.title(title)

    if xLabel:
        pyplot.xlabel(xLabel)

    if yLabel:
        pyplot.ylabel(yLabel)

    if filename:
        pyplot.savefig(filename)
    else:
        pyplot.show()

    pyplot.close()


def createMultiGraphWithVariance(ysMin=None, ysMax=None, title=None, xLabel=None, yLabel=None, filename=None, xs=None, ysDoubleArray=None, ysDeviationDoubleArray=None, colors=['b', 'k', 'r', 'm', 'g'], labels=None):
    pyplot.figure(figsize=(15, 15))

    if ysMin is not None and ysMax is not None:
        pyplot.ylim([ysMin, ysMax])

    for idx, ys in enumerate(ysDoubleArray):
        if labels is not None:
            label = labels[idx]
        else:
            label = None

        pyplot.plot(xs, ys, colors[idx] + '-', label=label)

    for idx, ysDeviation in enumerate(ysDeviationDoubleArray):
        deviationUp   = map(add, ysDoubleArray[idx], ysDeviation)
        deviationDown = map(sub, ysDoubleArray[idx], ysDeviation)

        pyplot.plot(xs, deviationUp,   colors[idx] + '--')
        pyplot.plot(xs, deviationDown, colors[idx] + '--')

    pyplot.legend(loc='best', prop={'size': 11})

    if title:
        pyplot.title(title)

    if xLabel:
        pyplot.xlabel(xLabel)

    if yLabel:
        pyplot.ylabel(yLabel)

    if filename:
        pyplot.savefig(filename)
    else:
        pyplot.show()

    pyplot.close()



def getCDFYValuesFromDict(input):
    sortedValues = sorted(input.values())

    return numpy.arange(len(sortedValues)) / float(len(sortedValues) - 1)


def createCDFGraph(input, xsMin, xsMax, title=None, xLabel=None, yLabel=None, filename=None, style='b-'):
    pyplot.figure(figsize=(15, 15))

    if xsMin is not None and xsMax is not None:
        pyplot.xlim([xsMin, xsMax])

    if title:
        pyplot.title(title)

    if xLabel:
        pyplot.xlabel(xLabel)

    if yLabel:
        pyplot.ylabel(yLabel)

    pyplot.plot(sorted(input.values()), getCDFYValuesFromDict(input), style)

    if filename:
        pyplot.savefig(filename)
    else:
        pyplot.show()

    pyplot.close()


def getPDFYValuesFromDict(input, numberOfBins=12):
    sortedValues = sorted(input.values())

    p, x = numpy.histogram(sortedValues, numberOfBins)
    x = x[:-1] + (x[1] - x[0]) / 2           # convert bin edges to centers
    p = [float(prob) / sum(p) for prob in p] # divide every element by sum to get [0,1) range

    return x.tolist(), p


def createPDFGraph(input, xsMin, xsMax, title=None, xLabel=None, yLabel=None, filename=None, color='b', numberOfBins=12):
    pyplot.figure(figsize=(15, 15))

    if xsMin is not None and xsMax is not None:
        pyplot.xlim([xsMin, xsMax])

    pyplot.ylim([0, 1])

    if title:
        pyplot.title(title)

    if xLabel:
        pyplot.xlabel(xLabel)

    if yLabel:
        pyplot.ylabel(yLabel)

    x, p = getPDFYValuesFromDict(input, numberOfBins)

    pyplot.bar(x, p, color=color)

    if filename:
        pyplot.savefig(filename)
    else:
        pyplot.show()

    pyplot.close()


def visualizeMetricOverTime(inputFilePath, outputFolderName, leagueName, delimiter=','):
    if not os.path.exists(outputFolderName):
        os.makedirs(outputFolderName)

    # read the data from CSV output of networkAnalyzr
    rownum = 0
    with open(inputFilePath, 'rb') as f:
        reader = csv.reader(f, delimiter=delimiter)

        for row in reader:
            # skip header
            if rownum == 0:
                rownum += 1
            else:
                metric           = row[0]
                competitionStage = row[1]
                seasons          = row[2].split('_')

                pageRankIdx = 0

                alphas = list()

                nodesList = list()
                edgesList = list()

                degreesList = list()
                degreesStdDeviationList = list()
                degreesStdErrorOfMeanList = list()
                degreeStrengthsList = list()
                degreeStrengthsStdDeviationList = list()
                degreeStrengthsStdErrorOfMeanList = list()

                inDegreesList = list()
                inDegreesStdDeviationList = list()
                inDegreesStdErrorOfMeanList = list()
                inDegreeStrengthsList = list()
                inDegreeStrengthsStdDeviationList = list()
                inDegreeStrengthsStdErrorOfMeanList = list()

                outDegreesList = list()
                outDegreesStdDeviationList = list()
                outDegreesStdErrorOfMeanList = list()
                outDegreeStrengthsList = list()
                outDegreeStrengthsStdDeviationList = list()
                outDegreeStrengthsStdErrorOfMeanList = list()

                pageRanksDoubleList = dict()
                pageRanksStdDeviationDoubleList = dict()
                pageRanksStdErrorOfMeanDoubleList = dict()
                pageRankEntropiesDoubleList = dict()
                pageRankRelativeEntropiesDoubleList = dict()

                if metric == 'nodes':
                    nodesList = row[3].split('_')

                elif metric == 'edges':
                    edgesList = row[3].split('_')

                elif metric == 'degrees':
                    degrees = row[3].split('_')

                    degreesList.append(sum(degrees) / float(len(degrees)))
                    degreesStdDeviationList.append(numpy.std(numpy.array(degrees), ddof=1))
                    degreesStdErrorOfMeanList.append(stats.sem(numpy.array(degrees)))

                elif metric == 'degreeStrengths':
                    degreeStrengths = row[3].split('_')

                    degreeStrengthsList.append(sum(degrees) / float(len(degreeStrengths)))
                    degreeStrengthsStdDeviationList.append(numpy.std(numpy.array(degreeStrengths), ddof=1))
                    degreeStrengthsStdErrorOfMeanList.append(stats.sem(numpy.array(degreeStrengths)))

                elif metric == 'inDegrees':
                    inDegrees = row[3].split('_')

                    inDegreesList.append(sum(inDegrees) / float(len(inDegrees)))
                    inDegreesStdDeviationList.append(numpy.std(numpy.array(inDegrees), ddof=1))
                    inDegreesStdErrorOfMeanList.append(stats.sem(numpy.array(inDegrees)))

                elif metric == 'inDegreeStrengths':
                    inDegreeStrengths = row[3].split('_')

                    inDegreeStrengthsList.append(sum(inDegreeStrengths) / float(len(inDegreeStrengths)))
                    inDegreeStrengthsStdDeviationList.append(numpy.std(numpy.array(inDegreeStrengths), ddof=1))
                    inDegreeStrengthsStdErrorOfMeanList.append(stats.sem(numpy.array(inDegreeStrengths)))

                elif metric == 'outDegrees':
                    outDegrees = row[3].split('_')

                    outDegreesList.append(sum(outDegrees) / float(len(outDegrees)))
                    outDegreesStdDeviationList.append(numpy.std(numpy.array(outDegrees), ddof=1))
                    outDegreesStdErrorOfMeanList.append(stats.sem(numpy.array(outDegrees)))

                elif metric == 'outDegreeStrengths':
                    outDegreeStrengths = row[3].split('_')

                    outDegreeStrengthsList.append(sum(outDegreeStrengths) / float(len(outDegreeStrengths)))
                    outDegreeStrengthsStdDeviationList.append(numpy.std(numpy.array(outDegreeStrengths), ddof=1))
                    outDegreeStrengthsStdErrorOfMeanList.append(stats.sem(numpy.array(outDegreeStrengths)))

                elif metric == 'pageRank':
                    pageRanks     = row[3].split('_')
                    alpha         = row[4]
                    numberOfNodes = row[5]

                    if alpha is constants.stdPageRankAlpha:
                        stdPageRankIdx = pageRankIdx

                    maxY     = 0
                    maxError = 0

                    alphas.append(alpha)

                    pageRanksDoubleList.append(list())
                    pageRanksStdDeviationDoubleList.append(list())
                    pageRanksStdErrorOfMeanDoubleList.append(list())
                    pageRankEntropiesDoubleList.append(list())
                    pageRankRelativeEntropiesDoubleList.append(list())

                    for pageRank in pageRanks:
                        averagePageRank        = sum(pageRank) / float(len(pageRank))
                        stdDevPageRank         = numpy.std(numpy.array(pageRank), ddof=1)
                        stdErrorOfMeanPageRank = stats.sem(numpy.array(pageRank))

                        pageRanksDoubleList[pageRankIdx].append(averagePageRank)
                        pageRanksStdDeviationDoubleList[pageRankIdx].append(stdDevPageRank)
                        pageRanksStdErrorOfMeanDoubleList[pageRankIdx].append(stdErrorOfMeanPageRank)

                        if pageRank > 0:
                            entropy = -pageRank * math.log(pageRank, 2)
                        else:
                            print "[Visualizer]  Entropy is ZERO!"
                            entropy = 0

                        averageEntropy         = sum(pageRankEntropiesDoubleList[pageRankIdx]) / len(pageRankEntropiesDoubleList[pageRankIdx])
                        averageRelativeEntropy = averageEntropy / math.log(numberOfNodes, 2)

                        pageRankEntropiesDoubleList[pageRankIdx].append(averageEntropy)
                        pageRankRelativeEntropiesDoubleList[pageRankIdx].append(averageRelativeEntropy)

                        if averagePageRank > maxY:
                            maxY = averagePageRank

                        if stdDevPageRank > maxError:
                            maxError = stdDevPageRank
                        if stdErrorOfMeanPageRank > maxError:
                            maxError = stdErrorOfMeanPageRank

                    pageRankIdx += 1

                else:
                    print "[Visualizer]  Unsupported property!"
                    return 1

    # reading of CSV done, plot everything
    colors = ['b', 'k', 'r', 'm', 'g']
    labels = ['alpha: ' + str(alpha) for alpha in alphas]

    filename = outputFolderName + 'nodes_over_time_' + competitionStage
    createDoubleGraphWithVariance(0, max(nodesList) + 1, 'Nodes over time ' + competitionStage,
                                  'Season', 'Nodes', filename,
                                  seasons, nodesList, [])

    filename = outputFolderName + 'nodes_edges_over_time_' + competitionStage
    createDoubleGraphWithVariance(0, max(nodesList + edgesList) + 1,
                                  'Nodes and Edges over time ' + competitionStage,
                                  'Season', 'Nodes/Edges', filename,
                                  seasons, nodesList, edgesList)

    filename = outputFolderName + 'degrees_over_time_' + competitionStage
    createDoubleGraphWithVariance(0, max(map(add, degreesList, degreesStdErrorOfMeanList) +
                                         map(add, degreeStrengthsList, degreeStrengthsStdErrorOfMeanList)),
                                  'Degrees over time ' + leagueName + ' ' + competitionStage,
                                  'Season', 'Degrees/Degree Strengths', filename,
                                  seasons, degreesList, degreeStrengthsList, degreesStdErrorOfMeanList,
                                  degreeStrengthsStdErrorOfMeanList)
    filename = outputFolderName + 'in_degrees_over_time_' + competitionStage

    createDoubleGraphWithVariance(0, max(map(add, inDegreesList, inDegreesStdErrorOfMeanList) +
                                         map(add, inDegreeStrengthsList,inDegreeStrengthsStdErrorOfMeanList)),
                                  'In Degrees over time ' + leagueName + ' ' + competitionStage,
                                  'Season', 'In Degrees/In Degree Strengths', filename,
                                  seasons, inDegreesList, inDegreeStrengthsList,
                                  inDegreesStdErrorOfMeanList, inDegreeStrengthsStdErrorOfMeanList)

    filename = outputFolderName + 'out_degrees_over_time_' + competitionStage
    createDoubleGraphWithVariance(0, max(map(add, outDegreesList, outDegreesStdErrorOfMeanList) +
                                         map(add, outDegreeStrengthsList, outDegreeStrengthsStdErrorOfMeanList)),
                                  'Out Degrees over time ' + leagueName + ' ' + competitionStage,
                                  'Season', 'Out Degrees/Out Degree Strengths', filename,
                                  seasons, outDegreesList, outDegreeStrengthsList,
                                  outDegreesStdErrorOfMeanList, outDegreeStrengthsStdErrorOfMeanList)

    filename = outputFolderName + 'pageRank_over_time_' + competitionStage
    createDoubleGraphWithVariance(0, max(map(add, pageRanksDoubleList[stdPageRankIdx], pageRanksStdErrorOfMeanDoubleList[stdPageRankIdx])),
                                  'PageRank over time ' + leagueName + ' ' + competitionStage,
                                  'Season', 'PageRank', filename,
                                  seasons, pageRanksDoubleList[stdPageRankIdx], [],
                                  pageRanksStdErrorOfMeanDoubleList[stdPageRankIdx], [])

    filename = outputFolderName + 'pageRank_over_time_multiAlpha_' + competitionStage
    # multi alpha PageRank average and std deviation/error of the mean over time
    createMultiGraphWithVariance(0, maxY + maxError,
                                 'Average PageRank ' + leagueName + ' ' + competitionStage,
                                 'Season', 'Average PageRank', filename,
                                 seasons, pageRanksDoubleList, pageRanksStdErrorOfMeanDoubleList, colors,
                                 labels)

    # multi alpha PageRank std deviation over time
    createMultiGraph(0, max(max(arr[1:]) for arr in pageRanksStdDeviationDoubleList), False,
                     'PageRank STD dev ' + leagueName + ' ' + competitionStage,
                     'Season', 'PageRank STD dev', filename + '_std_dev',
                     seasons, pageRanksStdDeviationDoubleList, colors, labels)

    # multi alpha PageRank entropy over time
    createMultiGraph(0, max(max(arr[1:]) for arr in pageRankEntropiesDoubleList), False,
                     'PageRank Entropy ' + leagueName + ' ' + competitionStage,
                     'Season', 'Entropy', filename + '_entropy',
                     seasons, pageRankEntropiesDoubleList, colors, labels)

    # multi alpha PageRank relative entropy over time
    createMultiGraph(0, max(max(arr[1:]) for arr in pageRankRelativeEntropiesDoubleList), False,
                     'PageRank Rel. Entropy ' + leagueName + ' ' + competitionStage,
                     'Season', 'Rel. Entropy', filename + '_relative_entropy',
                     seasons, pageRankRelativeEntropiesDoubleList, colors, labels)
