import os
import csv
import time
import snap
import math
import numpy
import networkx as nx

from scipy import stats
from operator import add
from collections import deque, Counter

import utils
import constants
import networkBuilder

from Visualizer import visualizer


__author__ = '3buson'


### --- NETWORK ANALYSIS FUNCTIONS --- ###

# networkx analyzers

# TODO: MOVE VISUALIZER PART TO VISUALIZER
def analyzeNetworkPropertyOverTime(graphsDict, directed, weighted, property, competitionStage, leagueName, folderName=None, filenameCSV=None):
    if not os.path.exists(folderName):
        os.makedirs(folderName)

    graphs  = graphsDict.values()
    seasons = graphsDict.keys()

    ys1 = list()
    ys2 = list()

    ys1StdDeviation   = list()
    ys1StdErrorOfMean = list()

    ys2StdDeviation   = list()
    ys2StdErrorOfMean = list()

    file   = open(filenameCSV, 'a')
    writer = csv.writer(file)

    if property == 'nodes':
        filename = folderName + 'nodes_over_time_' + competitionStage

        for graph in graphs:
            ys1.append(graph.number_of_nodes())

        writer.writerow([property, 'Nodes', competitionStage, ' '.join(str(v) for v in ys1)])

        visualizer.createDoubleGraphWithVariance(0, max(ys1) + 1, 'Nodes over time ' + competitionStage,
                                            'Season', 'Nodes', filename,
                                            seasons, ys1, [])

    elif property == 'edges':
        filename = folderName + 'nodes_edges_over_time_' + competitionStage

        for graph in graphs:
            ys1.append(graph.number_of_nodes())
            ys2.append(graph.number_of_edges())

        writer.writerow([property, 'Edges', competitionStage, ' '.join(str(v) for v in ys2)])

        visualizer.createDoubleGraphWithVariance(0, max(ys1 + ys2) + 1, 'Nodes and Edges over time ' + competitionStage,
                                            'Season', 'Nodes/Edges', filename,
                                            seasons, ys1, ys2)
    elif property == 'degrees':
        filename = folderName + 'degrees_over_time_' + competitionStage

        for graph in graphs:
            degrees = graph.degree()

            ys1.append(sum(degrees.values()) / float(len(degrees.values())))
            ys1StdDeviation.append(numpy.std(numpy.array(degrees.values()), ddof=1))
            ys1StdErrorOfMean.append(stats.sem(numpy.array(degrees.values())))

            strengths = dict()
            for edge in graph.edges(data='weight'):
                # 'undirected' as we're looking at degrees in general
                # add the weight to both nodes of the edge
                if edge[1] in strengths:
                    strengths[edge[1]] += edge[2]
                else:
                    strengths[edge[1]] = edge[2]

                if edge[0] in strengths:
                    strengths[edge[0]] += edge[2]
                else:
                    strengths[edge[0]] = edge[2]

            ys2.append(sum(strengths.values()) / float(len(strengths.values())))
            ys2StdDeviation.append(numpy.std(numpy.array(strengths.values()), ddof=1))
            ys2StdErrorOfMean.append(stats.sem(numpy.array(strengths.values())))

        writer.writerow(['degrees', 'Degrees', competitionStage, ' '.join(str(v) for v in ys1)])
        writer.writerow(['degreesStdDev', 'Degrees STD dev', competitionStage, ' '.join(str(v) for v in ys1StdDeviation)])
        writer.writerow(['degreesErrorOfMean', 'Degrees STD Error of Mean', competitionStage, ' '.join(str(v) for v in ys1StdErrorOfMean)])

        writer.writerow(['degreeStrengths', 'Degree Strengths', competitionStage, ' '.join(str(v) for v in ys2)])
        writer.writerow(['degreeStrengthsStdDev', 'Degree Strengths STD dev', competitionStage, ' '.join(str(v) for v in ys2StdDeviation)])
        writer.writerow(['degreeStrengthsErrorOfMean', 'Degree Strengths STD Error of Mean', competitionStage, ' '.join(str(v) for v in ys2StdErrorOfMean)])

        visualizer.createDoubleGraphWithVariance(0, max(map(add, ys1, ys1StdErrorOfMean) + map(add, ys2, ys2StdErrorOfMean)),
                                            'Degrees over time ' + leagueName + ' ' + competitionStage,
                                            'Season', 'Degrees/Degree Strengths', filename,
                                            seasons, ys1, ys2, ys1StdErrorOfMean, ys2StdErrorOfMean)
    elif property == 'inDegrees':
        filename = folderName + 'in_degrees_over_time_' + competitionStage

        for graph in graphs:
            degrees = graph.in_degree()

            ys1.append(sum(degrees.values()) / float(len(degrees.values())))
            ys1StdDeviation.append(numpy.std(numpy.array(degrees.values()), ddof=1))
            ys1StdErrorOfMean.append(stats.sem(numpy.array(degrees.values())))

            strengths = dict()
            for edge in graph.edges(data='weight'):
                if edge[1] in strengths:
                    strengths[edge[1]] += edge[2]
                else:
                    strengths[edge[1]] = edge[2]

            ys2.append(sum(strengths.values()) / float(len(strengths.values())))
            ys2StdDeviation.append(numpy.std(numpy.array(strengths.values()), ddof=1))
            ys2StdErrorOfMean.append(stats.sem(numpy.array(strengths.values())))

        writer.writerow(['inDegrees', 'In Degrees', competitionStage, ' '.join(str(v) for v in ys1)])
        writer.writerow(['inDegreesStdDev', 'In Degrees STD dev', competitionStage, ' '.join(str(v) for v in ys1StdDeviation)])
        writer.writerow(['inDegreesErrorOfMean', 'In Degrees STD Error of Mean', competitionStage, ' '.join(str(v) for v in ys1StdErrorOfMean)])

        writer.writerow(['inDegreeStrengths', 'In Degree Strengths', competitionStage, ' '.join(str(v) for v in ys2)])
        writer.writerow(['inDegreeStrengthsStdDev', 'In Degree Strengths STD dev', competitionStage, ' '.join(str(v) for v in ys2StdDeviation)])
        writer.writerow(['inDegreeStrengthsErrorOfMean', 'In Degree Strengths STD Error of Mean', competitionStage, ' '.join(str(v) for v in ys2StdErrorOfMean)])

        visualizer.createDoubleGraphWithVariance(0, max(map(add, ys1, ys1StdErrorOfMean) + map(add, ys2, ys2StdErrorOfMean)),
                                            'In Degrees over time ' + leagueName + ' ' + competitionStage,
                                            'Season', 'In Degrees/In Degree Strengths', filename,
                                            seasons, ys1, ys2, ys1StdErrorOfMean, ys2StdErrorOfMean)
    elif property == 'outDegrees':
        filename = folderName + 'out_degrees_over_time_' + competitionStage

        for graph in graphs:
            degrees = graph.out_degree()

            ys1.append(sum(degrees.values()) / float(len(degrees.values())))
            ys1StdDeviation.append(numpy.std(numpy.array(degrees.values()), ddof=1))
            ys1StdErrorOfMean.append(stats.sem(numpy.array(degrees.values())))

            strengths = dict()
            for edge in graph.edges(data='weight'):
                if edge[0] in strengths:
                    strengths[edge[0]] += edge[2]
                else:
                    strengths[edge[0]] = edge[2]

            ys2.append(sum(strengths.values()) / float(len(strengths.values())))
            ys2StdDeviation.append(numpy.std(numpy.array(strengths.values()), ddof=1))
            ys2StdErrorOfMean.append(stats.sem(numpy.array(strengths.values())))

        writer.writerow(['outDegrees', 'Out Degrees', competitionStage, ' '.join(str(v) for v in ys1)])
        writer.writerow(['outDegreesStdDev', 'Out Degrees STD dev', competitionStage, ' '.join(str(v) for v in ys1StdDeviation)])
        writer.writerow(['outDegreesErrorOfMean', 'Out Degrees STD Error of Mean', competitionStage, ' '.join(str(v) for v in ys1StdErrorOfMean)])

        writer.writerow(['outDegreeStrengths', 'Out Degree Strengths', competitionStage, ' '.join(str(v) for v in ys2)])
        writer.writerow(['outDegreeStrengthsStdDev', 'Out Degree Strengths STD dev', competitionStage, ' '.join(str(v) for v in ys2StdDeviation)])
        writer.writerow(['outDegreeStrengthsErrorOfMean', 'Out Degree Strengths STD Error of Mean', competitionStage, ' '.join(str(v) for v in ys2StdErrorOfMean)])

        visualizer.createDoubleGraphWithVariance(0, max(map(add, ys1, ys1StdErrorOfMean) + map(add, ys2, ys2StdErrorOfMean)),
                                            'Out Degrees over time ' + leagueName + ' ' + competitionStage,
                                            'Season', 'Out Degrees/Out Degree Strengths', filename,
                                            seasons, ys1, ys2, ys1StdErrorOfMean, ys2StdErrorOfMean)

    elif property == 'pageRank':
        filename = folderName + 'pageRank_over_time_' + competitionStage

        # regular PageRank
        for graph in graphs:
            pageRank = calculatePageRank(graph, directed, weighted)

            ys1.append(sum(pageRank.values()) / float(len(pageRank.values())))
            ys1StdDeviation.append(numpy.std(numpy.array(pageRank.values()), ddof=1))
            ys1StdErrorOfMean.append(stats.sem(numpy.array(pageRank.values())))

        visualizer.createDoubleGraphWithVariance(0, max(map(add, ys1, ys1StdErrorOfMean)),
                                            'PageRank over time ' + leagueName + ' ' + competitionStage,
                                            'Season', 'PageRank', filename,
                                            seasons, ys1, [], ys1StdErrorOfMean, [])

        # multi PageRanks with different alpha
        ysCombined               = list()
        ysStdDeviationCombined   = list()
        ysStdErrorOfMeanCombined = list()
        entropyCombined          = list()
        relativeEntropyCombined  = list()
        stdDeviationCombined     = list()

        filename = folderName + 'pageRank_over_time_multiAlpha_' + competitionStage

        maxY = 0
        maxError = 0
        alphas = constants.allPageRankAlphas

        seasonsString = ' '.join(str(s) for s in seasons)

        idx = 0
        for alpha in alphas:
            ysCombined.append(list())
            ysStdDeviationCombined.append(list())
            ysStdErrorOfMeanCombined.append(list())
            entropyCombined.append(list())
            relativeEntropyCombined.append(list())
            stdDeviationCombined.append(list())

            for graph in graphs:
                pageRank = calculatePageRank(graph, directed, weighted, alpha)

                # average and deviations of PageRank
                average        = sum(pageRank.values()) / float(len(pageRank.values()))
                stdDeviation   = numpy.std(numpy.array(pageRank.values()), ddof=1)
                stdErrorOfMean = stats.sem(numpy.array(pageRank.values()))

                # entropy of PageRank
                entropy     = 0
                pageRankSum = sum(pageRank.values())
                for pageRankValue in pageRank.values():
                    p = pageRankValue / pageRankSum

                    if p > 0:
                        entropy += p * math.log(p, 2)
                    else:
                        print "[Network Analyzr]  Entropy is ZERO!"

                entropy         = -entropy
                relativeEntropy = entropy / math.log(graph.number_of_nodes(), 2)

                if average > maxY:
                    maxY = average

                if stdDeviation > maxError:
                    maxError = stdDeviation
                if stdErrorOfMean > maxError:
                    maxError = stdErrorOfMean

                ysCombined[idx].append(average)
                ysStdDeviationCombined[idx].append(stdDeviation)
                ysStdErrorOfMeanCombined[idx].append(stdErrorOfMean)
                entropyCombined[idx].append(entropy)
                relativeEntropyCombined[idx].append(relativeEntropy)
                stdDeviationCombined[idx].append(stdDeviation)

            writer.writerow(['pageRankAvg', 'Average PageRank', competitionStage, alpha, seasonsString, ' '.join(str(v) for v in ysCombined[idx])])
            writer.writerow(['pageRankAvgStdDev', 'PageRank STD dev', competitionStage, alpha, seasonsString, ' '.join(str(v) for v in ysStdDeviationCombined[idx])])
            writer.writerow(['pageRankAvgErrorOfMean', 'PageRank STD Error Of Mean', competitionStage, alpha, seasonsString, ' '.join(str(v) for v in ysStdErrorOfMeanCombined[idx])])

            writer.writerow(['pageRankEntropy', 'PageRank Entropy', competitionStage, alpha, seasonsString, ' '.join(str(v) for v in entropyCombined[idx])])
            writer.writerow(['pageRankRelativeEntropy', 'PageRank Rel. Entropy', competitionStage, alpha, seasonsString, ' '.join(str(v) for v in relativeEntropyCombined[idx])])

            idx += 1

        colors = ['b', 'k', 'r', 'm', 'g']
        labels = ['alpha: ' + str(alpha) for alpha in alphas]

        # multi alpha PageRank average and std deviation/error of the mean over time
        visualizer.createMultiGraphWithVariance(0, maxY + maxError, 'Average PageRank ' + leagueName + ' ' + competitionStage,
                                           'Season', 'Average PageRank', filename,
                                           seasons, ysCombined, ysStdErrorOfMeanCombined, colors, labels)

        # multi alpha PageRank std deviation over time
        visualizer.createMultiGraph(0, max(max(arr[1:]) for arr in stdDeviationCombined), False,
                               'PageRank STD dev ' + leagueName + ' ' + competitionStage,
                               'Season', 'PageRank STD dev', filename + '_std_dev',
                               seasons, stdDeviationCombined, colors, labels)

        # multi alpha PageRank entropy over time
        visualizer.createMultiGraph(0, max(max(arr[1:]) for arr in entropyCombined), False,
                               'PageRank Entropy ' + leagueName + ' ' + competitionStage,
                               'Season', 'Entropy', filename + '_entropy',
                               seasons, entropyCombined, colors, labels)

        # multi alpha PageRank relative entropy over time
        visualizer.createMultiGraph(0, max(max(arr[1:]) for arr in relativeEntropyCombined), False,
                               'PageRank Rel. Entropy ' + leagueName + ' ' + competitionStage,
                               'Season', 'Rel. Entropy', filename + '_relative_entropy',
                               seasons, relativeEntropyCombined, colors, labels)

    else:
        print "[Network Analyzr]  Unsupported property!"
        return 1

    file.close()


def analyzeNetworkProperties(graph, directed, weighted, seasonId, competitionStage, file=None, outputToCsv=False, printHeader=False):
    if nx.is_strongly_connected(graph):
        radius       = nx.radius(graph)
        diameter     = nx.diameter(graph)
        eccentricity = nx.eccentricity(graph)
        center       = nx.center(graph)
        periphery    = nx.periphery(graph)
    else:
        radius       = -1
        diameter     = -1
        eccentricity = -1
        center       = -1
        periphery    = -1

    density = nx.density(graph)

    print("[Network Analyzr]  Radius: %d"       % radius)
    print("[Network Analyzr]  Diameter: %d"     % diameter)
    print("[Network Analyzr]  Eccentricity: %s" % eccentricity)
    print("[Network Analyzr]  Center: %s"       % center)
    print("[Network Analyzr]  Periphery: %s"    % periphery)
    print("[Network Analyzr]  Density: %s"      % density)

    # Degrees
    degrees         = graph.degree()
    averageDegree   = sum(degrees.values()) / float(len(degrees.values()))
    degreeDeviation = numpy.std(numpy.array(degrees.values()), ddof=1)
    print "[Network Analyzr]  Average degree: %f"   % averageDegree
    print "[Network Analyzr]  Degree deviation: %f" % degreeDeviation

    if directed:
        inDegrees          = graph.in_degree()
        averageInDegree    = sum(inDegrees.values())  / float(len(inDegrees.values()))
        inDegreeDeviation  = numpy.std(numpy.array(inDegrees.values()), ddof=1)
        outDegrees         = graph.out_degree()
        averageOutDegree   = sum(outDegrees.values()) / float(len(outDegrees.values()))
        outDegreeDeviation = numpy.std(numpy.array(outDegrees.values()), ddof=1)

        print "[Network Analyzr]  Average in degree: %f"    % averageInDegree
        print "[Network Analyzr]  In degree deviation: %f"  % inDegreeDeviation
        print "[Network Analyzr]  Average out degree: %f"   % averageOutDegree
        print "[Network Analyzr]  Out degree deviation: %f" % outDegreeDeviation

    # LCC
    numOfNodes = graph.number_of_nodes()
    if directed:
        lcc     = max(nx.strongly_connected_component_subgraphs(graph), key=len)
        lccSize = len(lcc)
    else:
        lcc     = max(nx.connected_component_subgraphs(graph), key=len)
        lccSize = len(lcc)

    lccFraction = lccSize / float(numOfNodes)

    print "[Network Analyzr]  Percentage of nodes in LCC: %f" % lccFraction

    # Clustering
    if not directed:
        print "[Analyzer]  Calculating average clustering..."
        averageClustering = nx.average_clustering(graph)
        print "[Analyzer]  Average clustering: %f" % averageClustering

    # Average Shortest Path Length
    pathLengths = []

    for node in graph.nodes():
        spl = nx.single_source_shortest_path_length(graph, node)

        for path in spl.values():
            pathLengths.append(path)

    avgSPL = sum(pathLengths) / float(len(pathLengths))

    print "[Network Analyzr]  Average shortest path length: %s" % avgSPL

    # Histogram of path lengths
    dist = {}
    for p in pathLengths:
        if p in dist:
            dist[p] += 1
        else:
            dist[p] = 1

    print("[Network Analyzr]  Length\t#Paths")

    vertices = dist.keys()
    for d in sorted(vertices):
        print '[Network Analyzr]  \t%s\t\t%d' % (d,dist[d])

    pageRank          = calculatePageRank(graph, directed, weighted)
    pageRankMean      = sum(pageRank.values()) / len(pageRank)
    pageRankDeviation = numpy.std(numpy.array(pageRank.values()), ddof=1)

    print "[Network Analyzr]  PageRank mean: %f"      % pageRankMean
    print "[Network Analyzr]  PageRank deviation: %f" % pageRankDeviation


    betweennessCentrality          = calculateBetweennessCentrality(graph)
    betweennessCentralityMean      = sum(betweennessCentrality.values()) / len(betweennessCentrality)
    betweennessCentralityDeviation = numpy.std(numpy.array(betweennessCentrality.values()), ddof=1)

    print "[Network Analyzr]  Betweenness centrality mean: %f"       % betweennessCentralityMean
    print "[Network Analyzr]  Betweenness centrality  deviation: %f" % betweennessCentralityDeviation


    bridgenessCentrality          = calculateBridgenessCentrality(graph)
    bridgenessCentralityMean      = sum(bridgenessCentrality.values()) / len(bridgenessCentrality)
    bridgenessCentralityDeviation = numpy.std(numpy.array(bridgenessCentrality.values()), ddof=1)

    print "[Network Analyzr]  Bridgeness centrality  mean: %f"      % bridgenessCentralityMean
    print "[Network Analyzr]  Bridgeness centrality  deviation: %f" % bridgenessCentralityDeviation

    # Output
    if outputToCsv:
        if printHeader:
            if directed:
                file.write("seasonId,stage,radius,diameter,avgDegree,degreeDeviation,"
                           "avgInDegree,inDegreeDeviation,avgOutDegree,outDegreeDeviation,"
                           "lccPercent,avgShortestPath,pageRankMean,pageRankDeviation,"
                           "betweennessMean,betweennessDeviation,bridgenessMean,bridgenessDeviation\n")
            else:
                file.write("seasonId,stage,radius,diameter,avgDegree,degreeDeviation,"
                           "lccPercent,avgClustering,avgShortestPath,"
                           "pageRankMean,pageRankDeviation,betweennessMean,"
                           "betweennessDeviation,bridgenessMean,bridgenessDeviation\n")

        if directed:
            file.write("%d,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n" %
                       (seasonId, competitionStage, radius, diameter, averageDegree, degreeDeviation,
                        averageInDegree, inDegreeDeviation, averageOutDegree, outDegreeDeviation,
                        lccFraction, avgSPL, pageRankMean, pageRankDeviation,
                        betweennessCentralityMean, betweennessCentralityDeviation,
                        bridgenessCentralityMean, bridgenessCentralityDeviation))
        else:
            file.write("%d,%s,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n" %
                       (seasonId, competitionStage, radius, diameter, averageDegree,
                        degreeDeviation, lccFraction, averageClustering, avgSPL,
                        pageRankMean, pageRankDeviation,
                        betweennessCentralityMean, betweennessCentralityDeviation,
                        bridgenessCentralityMean, bridgenessCentralityDeviation))


# TODO: MOVE VISUALIZER PART TO VISUALIZER
def analyzeDegrees(graph, directed, weighted, leagueString, seasonId, competitionStage, filenameCSV=None):
    inDegrees  = graph.in_degree()
    outDegrees = graph.out_degree()

    xs = range(0, graph.number_of_nodes())

    nodeLimit    = len(inDegrees.values())
    degreesLimit = max(inDegrees.values())
    numberOfBins = nodeLimit / 3

    file   = open(filenameCSV, 'a')
    writer = csv.writer(file)

    filenamePrefix = 'output/' + leagueString + '/graphs/bySeason/'
    filenameSuffix = ''

    # create 'output/graphs/bySeason' directory if it does not exist yet
    if not os.path.exists(filenamePrefix):
        os.makedirs(filenamePrefix)

    if weighted:
        filenameSuffix += '_weighted'

    if directed:
        filenameSuffix += '_directed'

        sumOfInDegrees = getSumOfDegrees(graph)
        sumOfOutDegrees = getSumOfDegrees(graph, False)

        # in degrees
        if not os.path.exists(filenamePrefix + 'inDegrees/' + competitionStage):
            os.makedirs(filenamePrefix + 'inDegrees/' + competitionStage)

        title    = 'In Degrees ' + `seasonId` + ' Stage: ' + competitionStage
        filename = filenamePrefix + 'inDegrees/' + competitionStage +\
                   '/inDegrees' + filenameSuffix + '_' + `seasonId` + '_stage_' + competitionStage

        visualizer.createGraph(xs, sorted(inDegrees.values(), reverse=True), 0, nodeLimit, 0, degreesLimit, 'b-',
                         False, title, 'Node', 'In Degree', filename)

        title = 'In Degrees Weight Sum' + `seasonId` + ' Stage: ' + competitionStage
        filename = filenamePrefix + 'inDegrees/' + competitionStage + \
                   '/inDegreesWeightSum' + filenameSuffix + '_' + `seasonId` + '_stage_' + competitionStage

        visualizer.createGraph(xs, sorted(sumOfInDegrees.values(), reverse=True), 0, nodeLimit, 0, degreesLimit, 'b-',
                               False, title, 'Node', 'In Degree Weight Sum', filename)

        # out degrees
        if not os.path.exists(filenamePrefix + 'outDegrees/' + competitionStage):
            os.makedirs(filenamePrefix + 'outDegrees/' + competitionStage)

        title    = 'Out Degrees ' + `seasonId` + ' Stage: ' + competitionStage
        filename = filenamePrefix + 'outDegrees/' + competitionStage +\
                   '/outDegrees' + filenameSuffix + '_' + `seasonId` + '_stage_' + competitionStage

        visualizer.createGraph(xs, sorted(outDegrees.values(), reverse=True), 0, nodeLimit, 0, degreesLimit, 'r-',
                         False, title, 'Node', 'Out Degree', filename)

        # degree distribution
        titleDistributionIn     = 'In Degrees Distribution ' + `seasonId` + ' Stage: ' + competitionStage
        filenameDistributionIn  = filenamePrefix + 'inDegrees/' + competitionStage +\
                                  '/inDegrees'  + filenameSuffix + '_distribution_' + `seasonId` + '_stage_' + competitionStage
        titleDistributionOut    = 'Out Degrees Distribution ' + `seasonId` + ' Stage: ' + competitionStage
        filenameDistributionOut = filenamePrefix + 'outDegrees/' + competitionStage +\
                                  '/outDegrees' + filenameSuffix + '_distribution_' + `seasonId` + '_stage_' + competitionStage

        inDegreeCount        = dict(Counter(inDegrees.values()))
        inDegreeCountKeys    = sorted(inDegreeCount, key=inDegreeCount.get)
        inDegreeCountValues  = sorted(inDegreeCount.values())
        outDegreeCount       = dict(Counter(outDegrees.values()))
        outDegreeCountKeys   = sorted(inDegreeCount, key=outDegreeCount.get)
        outDegreeCountValues = sorted(inDegreeCount.values())

        visualizer.createGraph(inDegreeCountKeys,  inDegreeCountValues,  0, degreesLimit, 0, degreesLimit / 5, 'b-',
                         False, titleDistributionIn,  'Degree', 'Node Count', filenameDistributionIn)
        visualizer.createGraph(outDegreeCountKeys, outDegreeCountValues, 0, degreesLimit, 0, degreesLimit / 5, 'r-',
                         False, titleDistributionOut, 'Degree', 'Node Count', filenameDistributionOut)

        # degree weight sum CDF & PDF
        titleCDFIn     = 'In Degrees CDF ' + `seasonId` + ' Stage: ' + competitionStage
        filenameCDFIn  = filenamePrefix + 'inDegrees/' + competitionStage + \
                        '/inDegrees' + filenameSuffix + '_CDF_' + `seasonId` + '_stage_' + competitionStage
        titleCDFOut    = 'Out Degrees CDF ' + `seasonId` + ' Stage: ' + competitionStage
        filenameCDFOut = filenamePrefix + 'outDegrees/' + competitionStage + \
                        '/outDegrees' + filenameSuffix + '_CDF_' + `seasonId` + '_stage_' + competitionStage
        titlePDFIn     = 'In Degrees PDF ' + `seasonId` + ' Stage: ' + competitionStage
        filenamePDFIn  = filenamePrefix + 'inDegrees/' + competitionStage + \
                        '/inDegrees' + filenameSuffix + '_PDF_' + `seasonId` + '_stage_' + competitionStage
        titlePDFOut    = 'Out Degrees PDF ' + `seasonId` + ' Stage: ' + competitionStage
        filenamePDFOut = filenamePrefix + 'outDegrees/' + competitionStage + \
                        '/outDegrees' + filenameSuffix + '_PDF_' + `seasonId` + '_stage_' + competitionStage

        visualizer.createCDFGraph(inDegrees,  0, degreesLimit, titleCDFIn,  'In Degree',  'Probability (CDF)', filenameCDFIn)
        visualizer.createCDFGraph(outDegrees, 0, degreesLimit, titleCDFOut, 'Out Degree', 'Probability (CDF)', filenameCDFOut, 'r-')

        visualizer.createPDFGraph(inDegrees,  0, degreesLimit, titlePDFIn,  'In Degree',  'Probability (PDF)', filenamePDFIn, numberOfBins=numberOfBins)
        visualizer.createPDFGraph(outDegrees, 0, degreesLimit, titlePDFOut, 'Out Degree', 'Probability (PDF)', filenamePDFOut, 'r', numberOfBins=numberOfBins)

        # degree weight sum CDF & PDF
        titleCDFWeightIn     = 'In Degrees Weight Sum CDF ' + `seasonId` + ' Stage: ' + competitionStage
        filenameCDFWeightIn  = filenamePrefix + 'inDegrees/' + competitionStage + \
                                '/inDegrees' + filenameSuffix + '_weight_sum_CDF_' + `seasonId` + '_stage_' + competitionStage
        titleCDFWeightOut    = 'Out Degrees Weight Sum CDF ' + `seasonId` + ' Stage: ' + competitionStage
        filenameCDFWeightOut = filenamePrefix + 'outDegrees/' + competitionStage + \
                                '/outDegrees' + filenameSuffix + '_weight_sum_CDF_' + `seasonId` + '_stage_' + competitionStage
        titlePDFWeightIn     = 'In Degrees Weight Sum PDF ' + `seasonId` + ' Stage: ' + competitionStage
        filenamePDFWeightIn  = filenamePrefix + 'inDegrees/' + competitionStage + \
                                '/inDegrees' + filenameSuffix + '_weight_sum_PDF_' + `seasonId` + '_stage_' + competitionStage
        titlePDFWeightOut    = 'Out Degrees Weight Sum PDF ' + `seasonId` + ' Stage: ' + competitionStage
        filenamePDFWeightOut = filenamePrefix + 'outDegrees/' + competitionStage + \
                                '/outDegrees' + filenameSuffix + '_weight_sum_PDF_' + `seasonId` + '_stage_' + competitionStage

        strengthsLimit = max(sumOfInDegrees)

        visualizer.createCDFGraph(sumOfInDegrees,  0, strengthsLimit, titleCDFWeightIn,  'In Degree Weight Sum',  'Probability (CDF)', filenameCDFWeightIn)
        visualizer.createCDFGraph(sumOfOutDegrees, 0, strengthsLimit, titleCDFWeightOut, 'Out Degree Weight Sum', 'Probability (CDF)', filenameCDFWeightOut, 'r-')

        visualizer.createPDFGraph(sumOfInDegrees,  0, strengthsLimit, titlePDFWeightIn,  'In Degree Weight Sum',  'Probability (PDF)', filenamePDFWeightIn, numberOfBins=numberOfBins)
        visualizer.createPDFGraph(sumOfOutDegrees, 0, strengthsLimit, titlePDFWeightOut, 'Out Degree Weight Sum', 'Probability (PDF)', filenamePDFWeightOut, 'r', numberOfBins=numberOfBins)

        writer.writerow(['inDegrees', 'In Degrees', competitionStage, seasonId, ' '.join(str(v) for v in inDegrees)])
        writer.writerow(['inDegreesSum', 'In Degree Weight Sum', competitionStage, seasonId, ' '.join(str(v) for v in sumOfInDegrees)])
        writer.writerow(['inDegreesKeysValues', 'In Degree Distribution', competitionStage, seasonId, ' '.join(str(v) for v in inDegreeCountKeys), ' '.join(str(v) for v in inDegreeCountValues)])

        writer.writerow(['outDegrees', 'Out Degrees', competitionStage, seasonId, ' '.join(str(v) for v in outDegrees)])
        writer.writerow(['outDegreesSum', 'Out Degree Weight Sum', competitionStage, seasonId, ' '.join(str(v) for v in sumOfOutDegrees)])
        writer.writerow(['outDegreesKeysValues', 'Out Degree Distribution', competitionStage, seasonId, ' '.join(str(v) for v in outDegreeCountKeys), ' '.join(str(v) for v in outDegreeCountValues)])

    file.close()


# TODO: MOVE VISUALIZER PART TO VISUALIZER
def analyzePageRank(graph, directed, weighted, leagueString, seasonId, competitionStage, multipleAlphas=False, filenameCSV=None):
    file   = open(filenameCSV, 'a')
    writer = csv.writer(file)

    if multipleAlphas:
        alphaValues = constants.allPageRankAlphas
    else:
        alphaValues = [constants.stdPageRankAlpha]

    for alpha in alphaValues:
        pageRank = calculatePageRank(graph, directed, weighted, alpha)

        xs = range(0, graph.number_of_nodes())

        nodeLimit      = len(pageRank.values())
        yLimitPageRank = max(pageRank.values()) * 1.05
        numberOfBins   = nodeLimit / 3

        filenamePrefix = 'output/' + leagueString + '/graphs/bySeason/'
        filenameSuffix = ''

        # create 'output/graphs/bySeason' directory if it does not exist yet
        if not os.path.exists(filenamePrefix):
            os.makedirs(filenamePrefix)

        if weighted:
            filenameSuffix += '_weighted'

        if directed:
            filenameSuffix += '_directed'

        filenameSuffix += '_alpha=' + str(alpha).replace('.', '_')

        # PageRank
        if not os.path.exists(filenamePrefix + 'pageRank/' + competitionStage):
            os.makedirs(filenamePrefix + 'pageRank/' + competitionStage)

        title                = 'PageRank ' + `seasonId` + ' Stage: ' + competitionStage + ' Alpha: ' + `alpha`
        filename             = filenamePrefix + 'pageRank/' + competitionStage +\
                               '/pageRank' + filenameSuffix + '_'              + `seasonId` + '_stage_' + competitionStage
        filenameDistribution = filenamePrefix + 'pageRank/' + competitionStage +\
                               '/pageRank' + filenameSuffix + '_distribution_' + `seasonId` + '_stage_' + competitionStage

        pageRankCount = dict(Counter(pageRank.values()))

        visualizer.createGraph(xs, sorted(pageRank.values(), reverse=True), 0, nodeLimit, 0, yLimitPageRank, 'k-',
                         False, title, 'Node Id',  'PageRank',  filename)
        visualizer.createGraph(pageRankCount.keys(), pageRankCount.values(), 0, nodeLimit, 0, yLimitPageRank, 'k-',
                         False, title, 'PageRank', 'NodeCount', filenameDistribution)

        # PageRank CDF & PDF
        titleCDFPageRank     = 'PageRank CDF ' + `seasonId` + ' Stage: ' + competitionStage + ' Alpha: ' + `alpha`
        filenameCDFPageRank  = filenamePrefix + 'pageRank/' + competitionStage + \
                               '/pageRank' + filenameSuffix + '_CDF_' + `seasonId` + '_stage_' + competitionStage
        titlePDFPageRank     = 'PageRank PDF ' + `seasonId` + ' Stage: ' + competitionStage + ' Alpha: ' + `alpha`
        filenamePDFPageRank  = filenamePrefix + 'pageRank/' + competitionStage + \
                               '/pageRank' + filenameSuffix + '_PDF_' + `seasonId` + '_stage_' +competitionStage

        visualizer.createCDFGraph(pageRank, 0, yLimitPageRank, titleCDFPageRank, 'PageRank',  'Probability (CDF)', filenameCDFPageRank, 'k-')
        visualizer.createPDFGraph(pageRank, 0, yLimitPageRank, titlePDFPageRank, 'PageRank',  'Probability (CDF)', filenamePDFPageRank, 'k', numberOfBins=numberOfBins)

        writer.writerow(['pageRank', 'PageRank', competitionStage, seasonId, alpha, ' '.join(str(v) for v in pageRank)])
        writer.writerow(['pageRankKeysValues', 'PageRank Distribution', competitionStage, seasonId, alpha, ' '.join(str(v) for v in pageRankCount.keys()), ' '.join(str(v) for v in pageRankCount.values())])

    file.close()


def getSumOfDegrees(graph, inDegrees=True):
    degreesSum = dict()

    for node in graph.nodes():
        degreeWeightSum = 0

        if inDegrees:
            for edge in graph.in_edges(node, data=True):
                degreeWeightSum += edge[2]['weight']
        else:
            for edge in graph.out_edges(node, data=True):
                degreeWeightSum += edge[2]['weight']

        degreesSum[node] = degreeWeightSum

    return degreesSum


def calculatePageRank(graph, directed, weighted, alpha=constants.stdPageRankAlpha):
    if utils.mode == 'debug':
        print "\n[Network Analyzr]  Calculating PageRank scores, alpha: %f" % alpha

    startTime  = time.time()
    ranking    = dict()
    newRanking = dict()
    maxiter    = 150
    tolerance  = 0.00001
    N          = graph.number_of_nodes()

    # set all ranking to 1 / N
    for node in graph.nodes():
        ranking[node]    = 1.0 / N
        newRanking[node] = 0

    iterations = 0

    while iterations < maxiter:
        if iterations % 10 == 0 and utils.mode == 'debug':
            print "[Network Analyzr]  Iteration %d" % iterations

        dp = 0

        for node in graph.nodes():
            if len(graph.neighbors(node)) == 0:
                dp += alpha * ranking[node] / N

        for node in graph.nodes():
            newRanking[node] = dp + ((1 - alpha) / N)

            if directed:
                predecessors = graph.predecessors(node)
            else:
                predecessors = graph.neighbors(node)

            # predecessors = graph.neighbors(node)

            for predecessor in predecessors:
                if directed:
                    successors = graph.successors(predecessor)
                else:
                    successors = graph.neighbors(predecessor)

                # successors = graph.neighbors(predecessor)

                if weighted:
                    weight = 0
                    numWeights = 0
                    for weightKey, weightDictValue in graph.get_edge_data(predecessor, node).iteritems():
                        weightValue = weightDictValue['weight']

                        # ignore ties
                        if weightValue != 0:
                            weight += weightValue
                            numWeights += 1

                    if numWeights != 0:
                        weight /= numWeights
                    else:
                        weight = 0
                else:
                    weight = 1

                newRanking[node] += alpha * ranking[predecessor] * weight / max(len(successors), 1)

        # check for convergence
        error = sum(abs(oldRankingValue - newRankingValue) for oldRankingValue, newRankingValue in zip(ranking.values(), newRanking.values()))
        if error <= tolerance:
            ranking = newRanking
            break

        ranking = newRanking.copy()

        iterations += 1

    timeSpent = time.time() - startTime

    if utils.mode == 'debug':
        print "[Network Analyzr]  PageRank calculation done, time spent: %f s\n" % timeSpent

    return ranking


def calculateBetweennessCentrality(graph):
    if utils.mode == 'debug':
        print "\n[Network Analyzr]  calculating Betweenness scores"

    startTime = time.time()
    cb        = dict()

    # initialize cb to zero
    for i in graph.nodes():
        cb[i] = 0

    for node in graph.nodes():
        if node % 500 == 0 and utils.mode == 'debug':
            print "[Network Analyzr]  Processed %d nodes" % (node)

        S = list()
        P = dict()
        Q = deque()

        sigma = dict()
        d     = dict()

        Q.append(node)

        # initialize structures for each node
        for i in graph.nodes():
            P[i]     = list()
            sigma[i] = 0
            d[i]     = -1

        sigma[node] = 1
        d[node]     = 0

        while len(Q) > 0:
            v = Q.popleft()
            S.append(v)

            for neighbor in graph.neighbors(v):
                # has neighbor been traversed before?
                if d[neighbor] < 0:
                    Q.append(neighbor)
                    d[neighbor] = d[v] + 1

                # is shortest path to neighbor through v?
                if d[neighbor] == d[v] + 1:
                    sigma[neighbor] += sigma[v]
                    P[neighbor].append(v)

        delta = dict()
        for i in graph.nodes():
            delta[i] = 0

        while len(S) > 0:
            w = S.pop()
            for v in P[w]:
                delta[v] += (sigma[v] / float(sigma[w])) * (1 + delta[w])
                if w != node:
                    cb[w] += delta[w]

    timeSpent = time.time() - startTime

    if utils.mode == 'debug':
        print "[Network Analyzr]  Betweenness calculation done, time spent: %f s\n" % timeSpent

    return cb


def calculateBridgenessCentrality(graph):
    if utils.mode == 'debug':
        print "\n[Network Analyzr]  calculating weighted Bridgeness scores"

    startTime = time.time()
    cb        = dict()

    # initialize cb to zero
    for i in graph.nodes():
        cb[i] = 0

    for node in graph.nodes():
        sp = nx.shortest_path_length(graph, node)

        if node % 500 == 0 and utils.mode == 'debug':
            print "[Network Analyzr]  Processed %d nodes" % (node)

        S = list()
        P = dict()
        Q = deque()

        sigma = dict()
        d     = dict()

        Q.append(node)

        # initialize structures for each node
        for i in graph.nodes():
            P[i]     = list()
            sigma[i] = 0
            d[i]     = -1

        sigma[node] = 1
        d[node]     = 0

        while len(Q) > 0:
            v = Q.popleft()
            S.append(v)

            for neighbor in graph.neighbors(v):
                # has neighbor been traversed before?
                if d[neighbor] < 0:
                    Q.append(neighbor)
                    d[neighbor] = d[v] + 1

                # is shortest path to neighbor through v?
                if d[neighbor] == d[v] + 1:
                    sigma[neighbor] += sigma[v]
                    P[neighbor].append(v)

        delta = dict()
        for i in graph.nodes():
            delta[i] = 0

        while len(S) > 0:
            w = S.pop()
            for v in P[w]:
                delta[v] += (sigma[v] / float(sigma[w])) * (1 + delta[w])
                if sp[w] > 1:
                    cb[w] += delta[w]

    timeSpent = time.time() - startTime

    if utils.mode == 'debug':
        print "[Network Analyzr]  Bridgeness calculation done, time spent: %f s\n" % timeSpent

    return cb


def analyzeMisc(FNGraph):
    # LCC, average distances, clustering
    tStart = time.time()

    print "[Network Analyzr]  Started calculating miscellaneous network statistics..."

    LCCPercentage = snap.GetMxWccSz(FNGraph) * 100.0
    print '\t[Network Analyzr]  Percentage of nodes in LCC: %.3f' % LCCPercentage

    clusteringCoefficient = snap.GetClustCf (FNGraph, -1)
    print "\t[Network Analyzr]  Clustering coefficient: %.3f" % clusteringCoefficient

    diameter= snap.GetBfsFullDiam(FNGraph, 1432, False)
    print "\t[Network Analyzr]  Network diameter: %.3f\n" % diameter

    # Average distance
    print "\t[Network Analyzr]  Calculating average distance..."

    i       = 0
    avgDist = 0
    nodes   = FNGraph.GetNodes()

    for sourceNode in FNGraph.Nodes():
        if i % 100 == 0 and utils.mode == 'debug':
            print "\t\tCalculated for %d nodes" % i

        NIdToDistH = snap.TIntH()
        snap.GetShortPath(FNGraph, sourceNode.GetId(), NIdToDistH)
        distanceSum = 0

        for destinationNode in NIdToDistH:
            distanceSum += NIdToDistH[destinationNode]

        avgDist += (1.0 / nodes) * float(distanceSum) / (nodes - 1)

        i += 1

    print "\t[Network Analyzr]  Network average distance: %.3f" % avgDist

    timeSpent = time.time() - tStart

    print "\n[Network Analyzr]  Finished calculating in %f seconds\n" % timeSpent


def createAndAnalyzeNetwork(leagueId, leagueString, seasonId, competitionStage, directed, weighted, simpleWeights, logWeights, file=None, outputToCsv=False, printHeader=False):
    clubsNetwork = networkBuilder.buildNetwork(leagueId, seasonId, competitionStage, directed, weighted, simpleWeights, logWeights)

    numberOfNodes = clubsNetwork.number_of_nodes()
    numberOfEdges = clubsNetwork.number_of_edges()

    print "\n[Network Analyzr]  Network successfully created"

    if utils.mode == 'debug':
        print "[Network Analyzr]  Number of nodes: %d" % numberOfNodes
        print "[Network Analyzr]  Number of edges: %d" % numberOfEdges

    filenamePrefix = 'output/'

    # create 'output/' directory if it does not exist yet
    if not os.path.exists(filenamePrefix):
        os.makedirs(filenamePrefix)

    filenameDegrees  = filenamePrefix + leagueString  + 'DegreesBySeason'  + '.csv'
    filenamePageRank = filenamePrefix + leagueString  + 'PageRankBySeason' + '.csv'

    if numberOfNodes > 0:
        analyzeDegrees(clubsNetwork, directed, weighted, leagueString, seasonId, competitionStage, filenameDegrees)
        analyzePageRank(clubsNetwork, directed, weighted, leagueString, seasonId, competitionStage, True, filenamePageRank)
    else:
        print "[Network Analyzr]  No matches matched the desired criteria, thus, network without nodes was created!"
        print "[Network Analyzr]  Did you enter the correct seasonId and/or leagueId?\n"


def createAndAnalyzeNetworksOverTime(leagueId, leagueString, seasons, competitionStage, directed, weighted, simpleWeights, logWeights):
    clubsNetworks = dict()

    filenamePrefix = 'output/'

    # create 'output/' directory if it does not exist yet
    if not os.path.exists(filenamePrefix):
        os.makedirs(filenamePrefix)

    filename = filenamePrefix + leagueString + ' NetworkPropertiesOverTime' + competitionStage.capitalize() + '.csv'

    # cleanup possible old files
    os.remove(filename) if os.path.exists(filename) else None

    for season in seasons:
        clubsNetwork = networkBuilder.buildNetwork(leagueId, season, competitionStage, directed, weighted, simpleWeights, logWeights)

        clubsNetworks[season] = clubsNetwork

        print "[Network Analyzr]  Network for season %s successfully created" % season

        if utils.mode == 'debug':
            print "[Network Analyzr]  Number of nodes: %d" % clubsNetwork.number_of_nodes()
            print "[Network Analyzr]  Number of edges: %d" % clubsNetwork.number_of_edges()

    for property in ['nodes', 'edges', 'degrees', 'inDegrees', 'outDegrees', 'pageRank']:
        print "[Network Analyzr]  Analyzing %s over time..." % property

        folderName = 'output/' + leagueString + '/graphs/overTime/' + competitionStage + '/'

        analyzeNetworkPropertyOverTime(clubsNetworks, directed, weighted, property, competitionStage, leagueString, folderName, filename)

        print "[Network Analyzr]  Analysis of %s over time done" % property

