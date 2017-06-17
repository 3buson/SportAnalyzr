import utils
import sportAnalyzr


__author__ = '3buson'


# LEAGUE IDS
# 1: Sweden Eliteserien Hockey League
# 2: Germany Bundesliga Handball League
# 3: Denmark Jack Handball League
# 4: Belgium Volleyball League
# 5: Germany Volleyball League
# 6: Greece Super League
# 7: Italy Serie A
# 8: National Hockey League
# 9: Italy Serie B
# 10: Portugal LPA Handball League
# 11: Scotland Premier League
# 12: Spain Liga Handball League
# 13: Poland Ekstraklasa Handball League
# 14: National Basketball Association
# 15: Germany DEL Hockey League
# 16: England Champions League
# 17: England Premier League
# 18: England League Two
# 19: England League One
# 20: Portugal Liga NOS
# 21: Switzerland NLA Hockey League
# 22: Spain LaLiga
# 23: Spain LaLiga 2
# 24: France Division Handball League
# 25: Russia KHL Hockey League
# 26: England Conference League
# 27: Turkey Super Lig
# 28: Greece A1 Basketball League
# 29: France Pro Volleyball League
# 30: Netherlands Eredevisie
# 31: Finland SM Hockey League
# 32: Scotland Champions League
# 33: Spain ACB Basketball League
# 34: Scotland League Two
# 35: Scotland League One
# 36: France Ligue 1
# 37: France Ligue 2
# 38: Norway Eliteserien Hockey League
# 39: Russia Superleague Basketball League
# 40: Italy Lega Basketball League
# 41: Poland Plusliga Volleyball League
# 42: Czech Hockey League
# 43: Belgium Pro League
# 44: Italy Serie Volleyball League
# 45: Turkey TBL Basketball League
# 46: Germany 2. Bundesliga
# 47: Germany 1. Bundesliga


def main():
    leagues = [7, 11, 14, 22, 36, 47]
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
        (156, 39, 176),
        (63, 81, 181),
        (3, 169, 244),
        (0, 150, 136),
        (205, 220, 57),
        (255, 235, 59),
        (255, 152, 0),
        (121, 85, 72),
        (158, 158, 158),
        (96, 125, 139),
        (233, 30, 99),
        (103, 58, 183),
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
