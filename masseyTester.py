import numpy
import utils
import constants
import masseyAnalyzr

from Visualizer import visualizer
from NetworkManipulator import networkBuilder
from NetworkManipulator import networkAnalyzr
from NetworkManipulator import correlationAnalyzr

__author__ = '3buson'


def main():
    # set log output level
    utils.mode = 'normal'

    # NBA + top football
    leagueIds = [14, 17, 22]
    seasonIds = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]

    isDirected = True
    isWeighted = True
    hasLogWeights = True
    hasSimpleWeights = False
    competitionStage = 'regular'

    masseyEntropies = dict()
    pageRankEntropies = dict()
    combinedMasseyEntropies = []
    combinedPageRankEntropies = []
    for leagueId in leagueIds:
        masseyEntropies[leagueId] = []
        pageRankEntropies[leagueId] = []

        for seasonId in seasonIds:
            network = networkBuilder.buildNetwork(leagueId, seasonId, competitionStage, isDirected, isWeighted, hasSimpleWeights, hasLogWeights)
            pageRank = networkAnalyzr.calculatePageRank(network, isDirected, isWeighted, constants.stdPageRankAlpha)
            relativePageRankEntropy, _ = networkAnalyzr.calculatePageRankRelativeEntropy(pageRank, network.number_of_nodes())
            combinedPageRankEntropies.append(relativePageRankEntropy)
            pageRankEntropies[leagueId].append(relativePageRankEntropy)

            relativeMasseyEntropy = masseyAnalyzr.calculateRelativeMasseyEntropy(leagueId, seasonId)
            combinedMasseyEntropies.append(relativeMasseyEntropy)
            masseyEntropies[leagueId].append(relativeMasseyEntropy)

    # Visualizations
    for leagueId in leagueIds:
        entropiesCombined = [pageRankEntropies[leagueId], masseyEntropies[leagueId]]
        visualizer.createMultiGraph(0.85, 1, False,
                                    'Primerjava relativne entropije PageRank in relativne entropije Masseyjeve ocene',
                                    'Sezona', 'Relativna entropija', 'output/massey_pr_entropy_' + str(leagueId), seasonIds, entropiesCombined,
                                    [(0, 0, 1), (1, 0, 0)], ['Relativna entropija ocene PageRank', 'Relativna entropije Masseyjeve ocene'])

    print "\n[Massey Tester]  Correlations:"

    for leagueId in leagueIds:
        print "\n[Massey Tester]  Correlation for league %d:" % leagueId

        [pearson, pp] = correlationAnalyzr.calculateCorrelation(pageRankEntropies[leagueId], masseyEntropies[leagueId], 'pearson')
        [spearman, sp] = correlationAnalyzr.calculateCorrelation(pageRankEntropies[leagueId], masseyEntropies[leagueId], 'spearman')

        print "[Massey Tester]  Paerson: %f, p=%f" % (pearson, pp)
        print "[Massey Tester]  Spearman: %f, p=%f" % (spearman, sp)

    [pearson, pp] = correlationAnalyzr.calculateCorrelation(combinedPageRankEntropies, combinedMasseyEntropies, 'pearson')
    [spearman, sp] = correlationAnalyzr.calculateCorrelation(combinedPageRankEntropies, combinedMasseyEntropies, 'spearman')

    print "\n[Massey Tester]  Combined correlation:"
    print "[Massey Tester]  Paerson: %f, p=%f" % (pearson, pp)
    print "[Massey Tester]  Spearman: %f, p=%f" % (spearman, sp)


if __name__ == "__main__":
    main()
