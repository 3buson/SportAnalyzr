__author__ = '3buson'

import sys
import time
import networkx as nx

def main():
    network = nx.erdos_renyi_graph(30, 0.3)

    pr1 = nx.pagerank(network)
    pr2 = calculatePageRank(network, False)

    print pr1
    print pr2

def calculatePageRank(graph, weighted, alpha=0.85):
    print "\n[Network Analyzr]  calculating PageRank scores"

    startTime  = time.time()
    ranking    = dict()
    newRanking = dict()
    maxiter    = 100
    tolerance  = 0.001
    N          = graph.number_of_nodes()

    # set all ranking to 1
    for node in graph.nodes():
        ranking[node]    = 1/ N
        newRanking[node] = 0

    iterations = 0

    while iterations < maxiter:
        if(iterations % 10 == 0):
            print "[Network Analyzr]  Iteration %d" % iterations

        dp = 0

        for node in graph.nodes():
            if len(graph.neighbors(node)) == 0:
                dp += alpha * ranking[node] / N

        for node in graph.nodes():
            newRanking[node] = dp + ((1 - alpha) / N)

            for neighbor in graph.neighbors(node):
                newRanking[node] += alpha * ranking[neighbor] / len(graph.neighbors(neighbor))

        # check for convergence
        if (sum(abs(oldRankingValue - newRankingValue) for oldRankingValue, newRankingValue in zip(ranking.values(), newRanking.values())) <= tolerance):
            ranking = newRanking
            break

        ranking = newRanking.copy()

        iterations += 1

    timeSpent = time.time() - startTime

    print "[Network Analyzr]  PageRank calculation done, time spent: %f s\n" % timeSpent

    return ranking


if __name__ == "__main__":
    main()
