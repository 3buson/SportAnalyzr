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
    leagues = [28, 33, 36, 37, 41, 43, 46, 48, 50]
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
        (166, 206, 227),
        (31, 120, 180),
        (178, 223, 138),
        (51, 160, 44),
        (251, 154, 153),
        (227, 26, 28),
        (253, 191, 111),
        (255, 127, 0),
        (202, 178, 214),
        (106, 61, 154),
        (255, 255, 153),
        (177, 89, 40)
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
