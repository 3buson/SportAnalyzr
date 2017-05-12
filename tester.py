import time
import networkx as nx

import utils
import sportAnalyzr


__author__ = '3buson'


# LEAGUE IDS
# 27: Greece Super League
# 28: Italy Serie A
# 29: National Hockey League
# 30: Italy Serie B
# 31: National Basketball Association
# 32: England Champions League
# 33: England Premier League
# 34: England League Two
# 35: England League One
# 36: Portugal Liga NOS
# 37: Spain LaLiga
# 38: Spain LaLiga 2
# 39: England Conference League
# 40: Turkey Super Lig
# 41: Netherlands Eredevisie
# 42: Scotland Champions League
# 43: Scotland Premier League
# 44: Scotland League Two
# 45: Scotland League One
# 46: France Ligue 1
# 47: France Ligue 2
# 48: Belgium Pro League
# 49: Germany 2. Bundesliga
# 50: Germany 1. Bundesliga


def main():
    leagues = [31, 28, 33, 37, 46, 50]
    seasonsInput = 'all'
    connection = utils.connectToDB()
    isDirected = True
    isWeighted = True
    analyzeBySeason = False
    analyzeOverTime = True
    hasLogWeights = True
    hasSimpleWeights = False
    printToFile = True
    printToCsv = False

    colors = [
        (244, 67, 54),
        (233, 30, 99),
        (156, 39, 176),
        (103, 58, 183),
        (63, 81, 181),
        (3, 169, 244),
        (0, 150, 136),
        (205, 220, 57),
        (255, 235, 59),
        (255, 152, 0),
        (121, 85, 72),
        (158, 158, 158),
        (96, 125, 139),
    ]

    # scale RGB values to the [0, 1] interval
    for i in range(len(colors)):
        r, g, b = colors[i]
        colors[i] = (r / 255.0, g / 255.0, b / 255.0)

    sportAnalyzr.analyze(connection, leagues, seasonsInput,
                         isDirected, isWeighted, analyzeBySeason, analyzeOverTime,
                         hasLogWeights, hasSimpleWeights, printToFile, printToCsv, colors)


if __name__ == "__main__":
    main()
