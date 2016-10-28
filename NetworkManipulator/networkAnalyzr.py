__author__ = '3buson'

import time
import snap
import networkx as nx
import matplotlib.pyplot as plt

from collections import deque

import networkBuilder


def createAndAnalyzeNetwork(leagueId, seasonId, directed, weighted):
    clubsNetwork = networkBuilder.buildNetwork(leagueId, seasonId, directed, weighted)

    print


def main():
    leagueId = 1

    seasonsInput  = raw_input('Please enter desired seasons separated by comma (all for all of them): ')
    directedInput = raw_input('Do you want to analyze a directed network? (0/1): ')
    weightedInput = raw_input('Do you want to analyze a weighted network? (0/1): ')

    if(seasonsInput.lower() == 'all'):
        seasons = seasonsInput
    else:
        seasons = seasonsInput.split(',')
        seasons = [int(season) for season in seasons]

    for seasonId in seasons:
        createAndAnalyzeNetwork(leagueId, seasonId, bool(directedInput), bool(weightedInput))


if __name__ == "__main__":
    main()


### ---- NETWORK ANALYSIS FUNCTIONS ---- ###

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
    for i in range(1, N):
        cb[i] = 0

    for node in graph.nodes():
        if(node % 500 == 0):
            print "[Network Analyzr]  Processed %d nodes" % (node)

        S = list()
        P = list()
        Q = deque()

        sigma = dict()
        d     = dict()

        Q.append(node)

        # initialize structures for each node
        for i in range(1, N):
            P.append(list())
            sigma[i] = 0
            d[i]     = -1

        # just append another empty list because nodes start with 1
        # we will never use P[0] but that's fine
        P.append(list())

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
        for i in range(1, N):
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
    for i in range(1, N):
        cb[i] = 0

    for node in graph.nodes():
        sp = nx.shortest_path_length(graph, node)

        if(node % 500 == 0):
            print "[Network Analyzr]  Processed %d nodes" % (node)

        S = list()
        P = list()
        Q = deque()

        sigma = dict()
        d     = dict()

        Q.append(node)

        # initialize structures for each node
        for i in range(1, N):
            P.append(list())
            sigma[i] = 0
            d[i]     = -1

        # just append another empty list because nodes start with 1
        # we will never use P[0] but that's fine
        P.append(list())

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
        for i in range(1, N):
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
