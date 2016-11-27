__author__ = '3buson'

import os
import sys
import time
import snap
import numpy
import networkx as nx

from scipy import stats
from matplotlib import pyplot
from operator import itemgetter
from collections import deque, Counter, OrderedDict

import networkBuilder

sys.path.insert(0, '../')
import utils
import constants


### ---- NETWORK ANALYSIS FUNCTIONS ---- ###

# networkx analyzers

def analyzeNetworkPropertyOverTime(graphsDict, weighted, property, competitionStage, folderName=None):
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

    if property == 'edges':
        filename = folderName + 'nodes_edges_over_time_' + competitionStage

        for graph in graphs:
            ys1.append(graph.number_of_nodes())
            ys2.append(graph.number_of_edges())

        utils.createDoubleGraphWithVariance(0, max(ys1 + ys2), 'Nodes and Edges over time ' + competitionStage,
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

        utils.createDoubleGraphWithVariance(0, max(ys1 + ys2), 'Degrees over time ' + competitionStage,
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

        utils.createDoubleGraphWithVariance(0, max(ys1 + ys2), 'In Degrees over time ' + competitionStage,
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

        utils.createDoubleGraphWithVariance(0, max(ys1 + ys2), 'Out Degrees over time ' + competitionStage,
                                            'Season', 'Out Degrees/Out Degree Strengths', filename,
                                            seasons, ys1, ys2, ys1StdErrorOfMean, ys2StdErrorOfMean)

    elif property == 'pageRank':
        filename = folderName + 'pageRank_over_time_' + competitionStage

        for graph in graphs:
            pageRank = calculatePageRank(graph, weighted)

            ys1.append(sum(pageRank.values()) / float(len(pageRank.values())))
            ys1StdDeviation.append(numpy.std(numpy.array(pageRank.values()), ddof=1))
            ys1StdErrorOfMean.append(stats.sem(numpy.array(pageRank.values())))

        utils.createDoubleGraphWithVariance(0, max(ys1), 'Page Rank over time ' + competitionStage,
                                            'Season', 'Page Rank', filename,
                                            seasons, ys1, [], ys1StdErrorOfMean, [])

    else:
        print "[Network Analyzr]  Unsupported property!"
        return 1


def analyzeNetworkProperties(graph, directed, weighted, seasonId, competitionStage, file=None, outputToCsv=False, printHeader=False):
    if (nx.is_strongly_connected(graph)):
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

    if (directed):
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
    if (directed):
        lcc     = max(nx.strongly_connected_component_subgraphs(graph), key=len)
        lccSize = len(lcc)
    else:
        lcc     = max(nx.connected_component_subgraphs(graph), key=len)
        lccSize = len(lcc)

    lccFraction = lccSize / float(numOfNodes)

    print "[Network Analyzr]  Percentage of nodes in LCC: %f" % lccFraction

    # Clustering
    if (not directed):
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

    pageRank          = calculatePageRank(graph, weighted)
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
    if (outputToCsv):
        if (printHeader):
            if (directed):
                file.write("seasonId,stage,radius,diameter,avgDegree,degreeDeviation,"
                           "avgInDegree,inDegreeDeviation,avgOutDegree,outDegreeDeviation,"
                           "lccPercent,avgShortestPath,pageRankMean,pageRankDeviation,"
                           "betweennessMean,betweennessDeviation,bridgenessMean,bridgenessDeviation\n")
            else:
                file.write("seasonId,stage,radius,diameter,avgDegree,degreeDeviation,"
                           "lccPercent,avgClustering,avgShortestPath,"
                           "pageRankMean,pageRankDeviation,betweennessMean,"
                           "betweennessDeviation,bridgenessMean,bridgenessDeviation\n")

        if (directed):
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


def analyzeDegrees(graph, directed, weighted, seasonId, competitionStage):
    inDegrees  = graph.in_degree()
    outDegrees = graph.out_degree()

    xs = range(0, graph.number_of_nodes())

    if competitionStage == 'playoff':
        nodeLimit       = 10
        degreesLimit    = 12
        strengthsLimit  = 15
    else:
        nodeLimit       = 30
        degreesLimit    = 75
        strengthsLimit  = 110

    filenamePrefix = 'output/graphs/bySeason/'
    filenameSuffix = ''

    # create 'output/graphs/bySeason' directory if it does not exist yet
    if not os.path.exists(filenamePrefix):
        os.makedirs(filenamePrefix)

    if (weighted):
        filenameSuffix += '_weighted'

    if (directed):
        filenameSuffix += '_directed'

        # in degrees
        if not os.path.exists(filenamePrefix + 'inDegrees/' + competitionStage):
            os.makedirs(filenamePrefix + 'inDegrees/' + competitionStage)

        title    = 'In Degrees ' + `seasonId` + ' Stage: ' + competitionStage
        filename = filenamePrefix + 'inDegrees/' + competitionStage +\
                   '/inDegrees' + filenameSuffix + '_' + `seasonId` + '_stage_' + competitionStage

        utils.createGraph(xs, sorted(inDegrees.values(), reverse=True), 0, nodeLimit, 0, degreesLimit, 'b-',
                         False, title, 'Node', 'In Degree', filename)

        # out degrees
        if not os.path.exists(filenamePrefix + 'outDegrees/' + competitionStage):
            os.makedirs(filenamePrefix + 'outDegrees/' + competitionStage)

        title    = 'Out Degrees ' + `seasonId` + ' Stage: ' + competitionStage
        filename = filenamePrefix + 'outDegrees/' + competitionStage +\
                   '/outDegrees' + filenameSuffix + '_' + `seasonId` + '_stage_' + competitionStage

        utils.createGraph(xs, sorted(outDegrees.values(), reverse=True), 0, nodeLimit, 0, degreesLimit, 'r-',
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

        utils.createGraph(inDegreeCountKeys,  inDegreeCountValues,  0, degreesLimit, 0, degreesLimit / 5, 'b-',
                         False, titleDistributionIn,  'Degree', 'Node Count', filenameDistributionIn)
        utils.createGraph(outDegreeCountKeys, outDegreeCountValues, 0, degreesLimit, 0, degreesLimit / 5, 'r-',
                         False, titleDistributionOut, 'Degree', 'Node Count', filenameDistributionOut)

        # degree weight sum CDF
        titleCDFIn     = 'In Degrees CDF ' + `seasonId` + ' Stage: ' + competitionStage
        filenameCDFIn  = filenamePrefix + 'inDegrees/' + competitionStage + \
                        '/inDegrees' + filenameSuffix + '_CDF_' + `seasonId` + '_stage_' + competitionStage
        titleCDFOut    = 'Out Degrees CDF ' + `seasonId` + ' Stage: ' + competitionStage
        filenameCDFOut = filenamePrefix + 'outDegrees/' + competitionStage + \
                        '/outDegrees' + filenameSuffix + '_CDF_' + `seasonId` + '_stage_' + competitionStage

        utils.createCDFGraph(inDegrees,  0, degreesLimit, titleCDFIn,  'In Degree',  'Probability (CDF)', filenameCDFIn)
        utils.createCDFGraph(outDegrees, 0, degreesLimit, titleCDFOut, 'Out Degree', 'Probability (CDF)', filenameCDFOut , 'r-')

        # degree weight sum CDF
        titleCDFWeightIn     = 'In Degrees Weight Sum CDF ' + `seasonId` + ' Stage: ' + competitionStage
        filenameCDFWeightIn  = filenamePrefix + 'inDegrees/' + competitionStage + \
                                '/inDegrees' + filenameSuffix + '_weight_sum_CDF_' + `seasonId` + '_stage_' + competitionStage
        titleCDFWeightOut    = 'Out Degrees Weight Sum CDF ' + `seasonId` + ' Stage: ' + competitionStage
        filenameCDFWeightOut = filenamePrefix + 'outDegrees/' + competitionStage + \
                                '/outDegrees' + filenameSuffix + '_weight_sum_CDF_' + `seasonId` + '_stage_' + competitionStage

        sumOfInDegrees  = getSumOfDegrees(graph)
        sumOfOutDegrees = getSumOfDegrees(graph, False)

        utils.createCDFGraph(sumOfInDegrees,  0, strengthsLimit, titleCDFWeightIn,  'In Degree Weight Sum',  'Probability (CDF)', filenameCDFWeightIn)
        utils.createCDFGraph(sumOfOutDegrees, 0, strengthsLimit, titleCDFWeightOut, 'Out Degree Weight Sum', 'Probability (CDF)', filenameCDFWeightOut , 'r-')


def analyzePageRank(graph, directed, weighted, seasonId, competitionStage, multipleAlphas=False):
    alphaValues = [0.85]

    if multipleAlphas:
        alphaValues.append(0.01)
        alphaValues.append(0.15)
        alphaValues.append(0.50)

    for alpha in alphaValues:
        pageRank = calculatePageRank(graph, weighted, alpha)

        xs = range(0, graph.number_of_nodes())

        if competitionStage == 'playoff':
            nodeLimit       = 10
            yLimitPageRank  = 0.15
        else:
            nodeLimit       = 30
            yLimitPageRank  = 0.085

        filenamePrefix = 'output/graphs/bySeason/'
        filenameSuffix = ''

        # create 'output/graphs/bySeason' directory if it does not exist yet
        if not os.path.exists(filenamePrefix):
            os.makedirs(filenamePrefix)

        if (weighted):
            filenameSuffix += '_weighted'

        if (directed):
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

        utils.createGraph(xs, sorted(pageRank.values(), reverse=True), 0, nodeLimit, 0, yLimitPageRank, 'k-',
                         False, title, 'Node Id',  'PageRank',  filename)
        utils.createGraph(pageRankCount.keys(), pageRankCount.values(), 0, nodeLimit, 0, yLimitPageRank, 'k-',
                         False, title, 'PageRank', 'NodeCount', filenameDistribution)

        # PageRank CDF
        titleCDFPageRank     = 'Page Rank CDF ' + `seasonId` + ' Stage: ' + competitionStage + ' Alpha: ' + `alpha`
        filenameCDFPageRank  = filenamePrefix + 'pageRank/' + competitionStage + \
                               '/pageRank' + filenameSuffix + '_CDF_' + `seasonId` + '_stage_' + competitionStage

        utils.createCDFGraph(pageRank, 0, yLimitPageRank, titleCDFPageRank, 'Page Rank',  'Probability (CDF)', filenameCDFPageRank)


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


def calculatePageRank(graph, weighted, alpha=0.85):
    print "\n[Network Analyzr]  calculating PageRank scores"

    startTime  = time.time()
    ranking    = dict()
    newRanking = dict()
    alpha      = 0.85
    maxiter    = 100
    tolerance  = 0.001


    # set all ranking to 1
    for node in graph.nodes():
        ranking[node] = 1

    iterations = 0

    while iterations < maxiter:
        if(iterations % 10 == 0):
            print "[Network Analyzr]  Iteration %d" % iterations

        totalSum = 0

        for i in graph.nodes():
            value = 0
            for j in graph.neighbors(i):
                if (weighted):
                    value += alpha * ranking[j] * graph[i][j].values()[0]['weight'] / graph.degree(j)
                else:
                    value += alpha * ranking[j] / graph.degree(j)

            totalSum += value
            newRanking[i] = value

        for k in graph.nodes():
            ranking[k] = ranking[k] + (1.0 - totalSum) / graph.number_of_nodes()

        # check for convergence
        if (abs(sum(ranking.values()) - sum(newRanking.values())) <= tolerance):
            ranking = newRanking
            break

        ranking = newRanking

        iterations += 1

    timeSpent = time.time() - startTime

    print "[Network Analyzr]  PageRank calculation done, time spent: %f s\n" % timeSpent

    return ranking


def calculateBetweennessCentrality(graph):
    print "\n[Network Analyzr]  calculating Betweenness scores"

    startTime = time.time()
    cb        = dict()

    # initialize cb to zero
    for i in graph.nodes():
        cb[i] = 0

    for node in graph.nodes():
        if(node % 500 == 0):
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
                if(d[neighbor] < 0):
                    Q.append(neighbor)
                    d[neighbor] = d[v] + 1

                # is shortest path to neighbor through v?
                if(d[neighbor] == d[v] + 1):
                    sigma[neighbor] += sigma[v]
                    P[neighbor].append(v)

        delta = dict()
        for i in graph.nodes():
            delta[i] = 0

        while len(S) > 0:
            w = S.pop()
            for v in P[w]:
                delta[v] += (sigma[v] / float(sigma[w])) * (1 + delta[w])
                if(w != node):
                    cb[w] += delta[w]

    timeSpent = time.time() - startTime

    print "[Network Analyzr]  Betweenness calculation done, time spent: %f s\n" % timeSpent

    return cb


def calculateBridgenessCentrality(graph):
    print "\n[Network Analyzr]  calculating weighted Bridgeness scores"

    startTime = time.time()
    cb        = dict()

    # initialize cb to zero
    for i in graph.nodes():
        cb[i] = 0

    for node in graph.nodes():
        sp = nx.shortest_path_length(graph, node)

        if(node % 500 == 0):
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
                if(d[neighbor] < 0):
                    Q.append(neighbor)
                    d[neighbor] = d[v] + 1

                # is shortest path to neighbor through v?
                if(d[neighbor] == d[v] + 1):
                    sigma[neighbor] += sigma[v]
                    P[neighbor].append(v)

        delta = dict()
        for i in graph.nodes():
            delta[i] = 0

        while len(S) > 0:
            w = S.pop()
            for v in P[w]:
                delta[v] += (sigma[v] / float(sigma[w])) * (1 + delta[w])
                if(sp[w] > 1):
                    cb[w] += delta[w]

    timeSpent = time.time() - startTime

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

    avgDist = 0
    i       = 0
    nodes   = FNGraph.GetNodes()

    for sourceNode in FNGraph.Nodes():
        if (i % 100 == 0):
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


def createAndAnalyzeNetwork(leagueId, seasonId, competitionStage, directed, weighted, logWeights, file=None, outputToCsv=False, printHeader=False):
    clubsNetwork = networkBuilder.buildNetwork(leagueId, seasonId, competitionStage, directed, weighted, logWeights)

    numberOfNodes = clubsNetwork.number_of_nodes()
    numberOfEdges = clubsNetwork.number_of_edges()

    print ''

    print "[Network Analyzr]  Network successfully created"
    print "[Network Analyzr]  Number of nodes: %d" % numberOfNodes
    print "[Network Analyzr]  Number of edges: %d" % numberOfEdges

    if numberOfNodes > 0:
        analyzeDegrees(clubsNetwork, directed, weighted, seasonId, competitionStage)
        analyzePageRank(clubsNetwork, directed, weighted, seasonId, competitionStage, True)
    else:
        print "[Network Analyzr]  No matches matched the desired criteria, thus, network without nodes was created!"
        print "[Network Analyzr]  Did you enter the correct seasonId and/or leagueId?"

    print ''


def createAndAnalyzeNetworksOverTime(leagueId, seasons, competitionStage, directed, weighted, logWeights):
    clubsNetworks = dict()

    for season in seasons:
        clubsNetwork = networkBuilder.buildNetwork(leagueId, season, competitionStage, directed, weighted, logWeights)

        clubsNetworks[season] = clubsNetwork

        print "[Network Analyzr]  Network for season %s successfully created" % season
        print "[Network Analyzr]  Number of nodes: %d" % clubsNetwork.number_of_nodes()
        print "[Network Analyzr]  Number of edges: %d" % clubsNetwork.number_of_edges()

    for property in ['edges', 'degrees', 'inDegrees', 'outDegrees', 'pageRank']:
        print "[Network Analyzr]  Analyzing %s over time..." % property

        folderName = 'output/graphs/overTime/' + competitionStage + '/'

        analyzeNetworkPropertyOverTime(clubsNetworks, weighted, property, competitionStage, folderName)

        print "[Network Analyzr]  Analysis of %s over time done" % property


def main():
    timeStart = time.time()

    file               = None
    leagueId           = 2
    outputFolderPrefix = 'output/'
    outputFileSuffix   = ''

    if not os.path.exists(outputFolderPrefix):
        os.makedirs(outputFolderPrefix)

    seasonsInput         = raw_input('Please enter desired seasons separated by comma (all for all of them): ')
    directedInput        = raw_input('Do you want to analyze a directed network? (0/1): ')
    weightedInput        = raw_input('Do you want to analyze a weighted network? (0/1): ')

    if (bool(int(weightedInput))):
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

    if (analyzeBySeason):
        printToFileInput = raw_input('Do you want to have output in a file? (0/1): ')
        printToFile      = bool(int(printToFileInput))
    else:
        printToFile = False

    if (printToFile):
        csvOutputInput = raw_input('Do you want to have output in a CSV? (0/1): ')
        printToCsv     = bool(int(csvOutputInput))

        outputFileBaseName = 'networkStats'

        if (isDirected):
            outputFileSuffix += '_directed'
        if (isWeighted):
            outputFileSuffix += '_weighted'

        if (printToCsv):
            file = open(outputFolderPrefix + outputFileBaseName + outputFileSuffix + '.csv', 'w')
        else:
            file = open(outputFolderPrefix + outputFileBaseName + outputFileSuffix + '.txt', 'w')
            sys.stdout = file

    if(seasonsInput.lower() == 'all'):
        seasons = constants.allSeasons
    else:
        seasons = seasonsInput.split(',')
        seasons = [int(season) for season in seasons]


    if (analyzeBySeason):
        index = 0
        for seasonId in seasons:
            print "\n[Network Analyzr] SEASON: %s" % seasonId

            createAndAnalyzeNetwork(leagueId, seasonId, 'all',     isDirected, isWeighted, hasLogWeights, file, printToCsv, not bool(index))
            createAndAnalyzeNetwork(leagueId, seasonId, 'regular', isDirected, isWeighted, hasLogWeights, file, printToCsv, not bool(index))
            createAndAnalyzeNetwork(leagueId, seasonId, 'playoff', isDirected, isWeighted, hasLogWeights, file, printToCsv, not bool(index))

            index += 1

            print ''

    if (analyzeOverTime):
        print "\n[Network Analyzr] Building networks for all seasons"

        createAndAnalyzeNetworksOverTime(leagueId, seasons, 'all',     isDirected, isWeighted, hasLogWeights)
        createAndAnalyzeNetworksOverTime(leagueId, seasons, 'regular', isDirected, isWeighted, hasLogWeights)
        createAndAnalyzeNetworksOverTime(leagueId, seasons, 'playoff', isDirected, isWeighted, hasLogWeights)

    timeSpent = time.time() - timeStart

    print "\n[Network Analyzr] Analysis done, time spent: %ds" % int(round(timeSpent))

    return 0


if __name__ == "__main__":
    main()