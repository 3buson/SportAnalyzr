import utils
import sportAnalyzr


__author__ = '3buson'


# LEAGUE IDS
# 2: Germany Bundesliga Handball League
# 3: Denmark Jack Handball League
# 10: Portugal LPA Handball League
# 12: Spain Liga Handball League
# 13: Poland Ekstraklasa Handball League
# 24: France Division Handball League

# 4: Belgium Volleyball League
# 5: Germany Volleyball League
# 29: France Pro Volleyball League
# 41: Poland Plusliga Volleyball League
# 44: Italy Serie Volleyball League

# 1: Sweden Eliteserien Hockey League
# 8: National Hockey League
# 15: Germany DEL Hockey League
# 21: Switzerland NLA Hockey League
# 25: Russia KHL Hockey League
# 31: Finland SM Hockey League
# 38: Norway Eliteserien Hockey League
# 42: Czech Hockey League

# 14: National Basketball Association
# 28: Greece A1 Basketball League
# 33: Spain ACB Basketball League
# 39: Russia Superleague Basketball League
# 40: Italy Lega Basketball League
# 45: Turkey TBL Basketball League

# 6: Greece Super League
# 7: Italy Serie A
# 9: Italy Serie B
# 11: Scotland Premier League
# 16: England Champions League
# 17: England Premier League
# 18: England League Two
# 19: England League One
# 20: Portugal Liga NOS
# 22: Spain LaLiga
# 23: Spain LaLiga 2
# 26: England Conference League
# 27: Turkey Super Lig
# 30: Netherlands Eredevisie
# 32: Scotland Champions League
# 34: Scotland League Two
# 35: Scotland League One
# 36: France Ligue 1
# 37: France Ligue 2
# 43: Belgium Pro League
# 46: Germany 2. Bundesliga
# 47: Germany 1. Bundesliga


def main():
    # NBA
    # leagues = [14]
    # top football
    # leagues = [7, 17, 22, 36, 47]
    # NBA + top football
    # leagues = [7, 14, 17, 22, 36, 47]
    # NBA + top football extended
    leagues = [7, 11, 14, 17, 20, 22, 27, 30, 36, 43, 47]
    # top football extended
    # leagues = [7, 11, 17, 20, 22, 27, 30, 36, 43, 47]
    # hockey
    # leagues = [1, 8, 15, 21, 25, 31, 38, 42]
    # handball
    # leagues = [2, 3, 10, 12, 13, 24]
    # volleyball
    # leagues = [4, 5, 29, 41, 44]
    # basketball
    # leagues = [14, 28, 33, 39, 40, 45]
    # various sports combined
    # leagues = [14, 28, 33, 17, 22, 2, 24, 29, 8, 25]

    # common seasons (various sports)
    # seasonsInput = '2008,2009,2010,2011'
    # common seasons (NBA + football)
    # seasonsInput = '2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014'
    # all seasons
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
