__author__ = '3buson'

import sys
import time
import snap
import numpy
import networkx as nx
import matplotlib.pyplot as plt

from collections import deque

import networkBuilder

sys.path.insert(0, '../')
import constants


### ---- NETWORK ANALYSIS FUNCTIONS ---- ###

# networkx analyzers

def analyzeNetworkProperties(graph, directed, seasonId, file=None, outputToCsv=False, printHeader=False):
    radius       = nx.radius(graph)
    diameter     = nx.diameter(graph)
    eccentricity = nx.eccentricity(graph)
    center       = nx.center(graph)
    periphery    = nx.periphery(graph)
    density      = nx.density(graph)

    print("[Network Analyzr]  Radius: %d"       % radius)
    print("[Network Analyzr]  Diameter: %d"     % diameter)
    print("[Network Analyzr]  Eccentricity: %s" % eccentricity)
    print("[Network Analyzr]  Center: %s"       % center)
    print("[Network Analyzr]  Periphery: %s"    % periphery)
    print("[Network Analyzr]  Density: %s"      % density)

    # Degrees
    degrees       = graph.degree()
    averageDegree = sum(degrees.values()) / float(len(degrees.values()))
    print "[Network Analyzr]  Average degree: %f" % averageDegree

    if (directed):
        inDegrees        = graph.in_degree()
        outDegrees       = graph.out_degree()
        averageInDegree  = sum(inDegrees.values())  / float(len(inDegrees.values()))
        averageOutDegree = sum(outDegrees.values()) / float(len(outDegrees.values()))
        print "[Network Analyzr]  Average in degree: %f"  % averageInDegree
        print "[Network Analyzr]  Average out degree: %f" % averageOutDegree

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

    # Average distance
    averageDistance = nx.average_shortest_path_length(lcc)
    print "[Network Analyzr]  Average distance: %f" % averageDistance

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

    pageRank          = calculatePageRank(graph)
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
                file.write("seasonId,radius,diameter,avgDegree,avgInDegree,avgOutDegree,lccPercent,avgDistance,avgShortestPath,pageRankMean,pageRankDeviation,betweennessMean,betweennessDeviation,bridgenessMean.bridgenessDeviation\n")
            else:
                file.write("seasonId,radius,diameter,avgDegree,lccPercent,avgDistance,avgClustering,avgShortestPath,pageRankMean,pageRankDeviation,betweennessMean,betweennessDeviation,bridgenessMean.bridgenessDeviation\n")

        if (directed):
            file.write("%d,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n" %
                       (seasonId, radius, diameter, averageDegree,
                        averageInDegree, averageOutDegree, lccFraction,
                        averageDistance, avgSPL, pageRankMean, pageRankDeviation,
                        betweennessCentralityMean, betweennessCentralityDeviation,
                        bridgenessCentralityMean, bridgenessCentralityDeviation))
        else:
            file.write("%d,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f\n" %
                       (seasonId, radius, diameter, averageDegree,
                        lccFraction, averageDistance,
                        averageClustering, avgSPL, pageRankMean, pageRankDeviation,
                        betweennessCentralityMean, betweennessCentralityDeviation,
                        bridgenessCentralityMean, bridgenessCentralityDeviation))


def calculatePageRank(graph):
    print "\n[Network Analyzr]  calculating PageRank scores"

    startTime  = time.time()
    ranking    = dict()
    newRanking = dict()

    # set all ranking to 1
    for node in graph.nodes():
        ranking[node] = 1

    iterations = 0

    # TODO: run until convergence...
    while iterations < 30:
        if(iterations % 10 == 0):
            print "[Network Analyzr]  Iteration %d" % iterations

        sum = 0

        for i in graph.nodes():
            value = 0
            for j in graph.neighbors(i):
                value += 0.85 * ranking[j] / graph.degree(j)

            sum += value
            newRanking[i] = value

        for k in graph.nodes():
            ranking[k] = ranking[k] + (1.0 - sum) / graph.number_of_nodes()

        ranking = newRanking

        iterations += 1

    timeSpent = time.time() - startTime

    print "[Network Analyzr]  PageRank calculation done, time spent: %f s\n" % timeSpent

    return ranking

def calculateBetweennessCentrality(graph):
    print "\n[Network Analyzr]  calculating Betweenness scores"

    startTime  = time.time()
    N          = graph.number_of_nodes() + 1
    cb         = dict()

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
    N         = graph.number_of_nodes() + 1
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

# SNAP analyzers

def analyzeDegrees(FNGraph):
    timeStart = time.time()

    print "[Network Analyzr]  Started analyzing network degrees: \n"

    DegToCntV = snap.TIntPrV()
    snap.GetDegCnt(FNGraph, DegToCntV)

    avgDeg  = 0
    xVector = list()
    yVector = list()

    for node in DegToCntV:
        avgDeg += int(node.GetVal2()) * int(node.GetVal1())

        xVector.append(node.GetVal1())
        yVector.append(node.GetVal2())

    avgDeg = avgDeg / FNGraph.GetNodes()

    print "\t[Network Analyzr]  Network average degree: %d" % avgDeg

    # plot degree distribution
    plt.figure(0)
    plt.plot(xVector, yVector, 'b-')
    plt.title("Degree distribution \n Average degree: %d" % avgDeg)
    plt.ylabel("Number of nodes")
    plt.xlabel("Degrees")
    plt.savefig('DegreeDistribution.png')

    timeSpent = time.time() - timeStart

    print "\n[Network Analyzr]  Finished calculating in %.3f seconds\n" % timeSpent


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


def createAndAnalyzeNetwork(leagueId, seasonId, directed, weighted, file=None, outputToCsv=False, printHeader=False):
    clubsNetwork = networkBuilder.buildNetwork(leagueId, seasonId, directed, weighted)

    numberOfNodes = clubsNetwork.number_of_nodes()
    numberOfEdges = clubsNetwork.number_of_edges()

    print ''

    print "[Network Analyzr]  Network successfully created"
    print "[Network Analyzr]  Number of nodes: %d" % numberOfNodes
    print "[Network Analyzr]  Number of edges: %d" % numberOfEdges

    if numberOfNodes > 0:
            analyzeNetworkProperties(clubsNetwork, directed, seasonId, file, outputToCsv, printHeader)
    else:
        print "[Network Analyzr]  No matches matched the desired criteria, thus, network without nodes was created!"
        print "[Network Analyzr]  Did you enter the correct seasonId and/or leagueId?"

    print ''


def main():
    file               = None
    leagueId           = 2
    outputFolderPrefix = 'output/'
    outputFileSuffix   = ''

    seasonsInput     = raw_input('Please enter desired seasons separated by comma (all for all of them): ')
    directedInput    = raw_input('Do you want to analyze a directed network? (0/1): ')
    weightedInput    = raw_input('Do you want to analyze a weighted network? (0/1): ')
    printToFileInput = raw_input('Do you want to have output in a file? (0/1): ')

    isDirectected = bool(int(directedInput))
    isWeighted    = bool(int(weightedInput))
    printToFile   = bool(int(printToFileInput))

    if (printToFile):
        csvOutputInput = raw_input('Do you want to have output in a CSV? (0/1): ')
        printToCsv     = bool(int(csvOutputInput))

        outputFileBaseName = 'networkStats'

        if (isDirectected):
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

    index = 0
    for seasonId in seasons:
        print "\n[Network Analyzr] SEASON: %s" % seasonId

        createAndAnalyzeNetwork(leagueId, seasonId, isDirectected, isWeighted, file, printToCsv, not bool(index))
        index += 1

        print ''


if __name__ == "__main__":
    main()