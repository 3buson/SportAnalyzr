__author__ = '3buson'


# --- VARIOUS CONSTANTS --- #
currentSeason       = '16'
inflationRatio      = 2.11
youngestAgeGroup    = 17
oldestAgeGroup      = 25
perspectiveAge      = 18
mostValuableAge     = 27
noRankingPenalty    = 25
noWeightPathPenalty = 1000
defaultClubWeight   = 0.1
allSeasons          = range(1976, 2015)
allLeagues          = range(1, 3)
stdPageRankAlpha    = 0.85
allPageRankAlphas   = [0.001, 0.15, 0.5, 0.85, 0.999]


# --- URLS --- #
urls = dict()

urls['NHL'] = {
    'baseUrl'    : 'http://www.hockey-reference.com/leagues/',
    'urlPrefix'  : 'NHL_',
    'urlSuffix'  : '_skaters-advanced.html',
    'urlSuffix2' : '_goalies.html'
}

urls['NBA'] = {
    'baseUrl'   : 'http://www.basketball-reference.com/leagues/',
    'urlPrefix' : 'NBA_',
    'urlSuffix' : '_advanced.html'
}


# --- LEAGUES --- #
leagues        = dict()

# basketball
leagues['NBA'] = 'National Basketball Association'
leagues['TUB'] = 'Turkey TBL Basketball League'
leagues['SPB'] = 'Spain ACB Basketball League'
leagues['ITB'] = 'Italy Lega Basketball League'
leagues['GRB'] = 'Greece A1 Basketball League'
leagues['RUB'] = 'Russia Superleague Basketball League'
# football
leagues['B1']  = 'Belgium Pro League'
leagues['G1']  = 'Greece Super League'
leagues['P1']  = 'Portugal Liga NOS'
leagues['T1']  = 'Turkey Super Lig'
leagues['N1']  = 'Netherlands Eredivisie'
leagues['I1']  = 'Italy Serie A'
leagues['I2']  = 'Italy Serie B'
leagues['D1']  = 'Germany 1. Bundesliga'
leagues['D2']  = 'Germany 2. Bundesliga'
leagues['F1']  = 'France Ligue 1'
leagues['F2']  = 'France Ligue 2'
leagues['SP1'] = 'Spain LaLiga'
leagues['SP2'] = 'Spain LaLiga 2'
leagues['E0']  = 'England Premier League'
leagues['E1']  = 'England Champions League'
leagues['E2']  = 'England League One'
leagues['E3']  = 'England League Two'
leagues['EC']  = 'England Conference League'
leagues['SC0'] = 'Scotland Premier League'
leagues['SC1'] = 'Scotland Champions League'
leagues['SC2'] = 'Scotland League One'
leagues['SC3'] = 'Scotland League Two'
# hockey
leagues['CZH'] = 'Czech Hockey League'
leagues['FIH'] = 'Finland SM Hockey League'
leagues['GEH'] = 'Germany DEL Hockey League'
leagues['NOH'] = 'Norway Eliteserien Hockey League'
leagues['RUH'] = 'Russia KHL Hockey League'
leagues['SWH'] = 'Sweden Eliteserien Hockey League'
leagues['CHH'] = 'Switzerland NLA Hockey League'
leagues['NHL'] = 'National Hockey League'
# handball
leagues['POH'] = 'Poland Ekstraklasa Handball League'
leagues['PRH'] = 'Portugal LPA Handball League'
leagues['GBH'] = 'Germany Bundesliga Handball League'
leagues['FRH'] = 'France Division Handball League'
leagues['DEH'] = 'Denmark Jack Handball League'
leagues['SPH'] = 'Spain Liga Handball League'
# volleyball
leagues['BEV'] = 'Belgium Volleyball League'
leagues['FRV'] = 'France Pro Volleyball League'
leagues['GEV'] = 'Germany Volleyball League'
leagues['ITV'] = 'Italy Serie Volleyball League'
leagues['POV'] = 'Poland Plusliga Volleyball League'


leagueNames = dict()
leagueNames['GER'] = 'Germany 1. Bundesliga'
leagueNames['FRA'] = 'France Ligue 1.'
leagueNames['BEL'] = 'Belgium Pro Liga'
leagueNames['ESP'] = 'Spain LaLiga'
leagueNames['TUR'] = 'Turkey Super Lig'
leagueNames['ENG'] = 'English Premier League'
leagueNames['SCO'] = 'Scotland Premier League'
leagueNames['ITA'] = 'Italy Serie A'
leagueNames['GRE'] = 'Greece Super League'
leagueNames['NBA'] = 'National Basketball League'
leagueNames['NED'] = 'Netherlands Eredivisie'


# --- CLUBS DICTS --- #

# NHL CLUBS DICT
clubDictNHL        = dict()
clubDictNHL['ANA'] = 'Anaheim Ducks'
clubDictNHL['ARI'] = 'Arizona Coyotes'
clubDictNHL['BOS'] = 'Boston Bruins'
clubDictNHL['BUF'] = 'Buffalo Sabres'
clubDictNHL['CAR'] = 'Carolina Hurricanes'
clubDictNHL['CBJ'] = 'Columbus Blue Jackets'
clubDictNHL['CGY'] = 'Calgary Flames'
clubDictNHL['CHI'] = 'Chicago Blackhawks'
clubDictNHL['COL'] = 'Colorado Avalanche'
clubDictNHL['DAL'] = 'Dallas Stars'
clubDictNHL['DET'] = 'Detroit Red Wings'
clubDictNHL['EDM'] = 'Edmonton Oilers'
clubDictNHL['FLA'] = 'Florida Panthers'
clubDictNHL['LAK'] = 'Los Angeles Kings'
clubDictNHL['MIN'] = 'Minnesota Wild'
clubDictNHL['MTL'] = 'Montreal Canadiens'
clubDictNHL['NJD'] = 'New Jersey Devils'
clubDictNHL['NSH'] = 'Nashville Predators'
clubDictNHL['NYI'] = 'New York Islanders'
clubDictNHL['NYR'] = 'New York Rangers'
clubDictNHL['OTT'] = 'Ottawa Senators'
clubDictNHL['PHI'] = 'Philadelphia Flyers'
clubDictNHL['PIT'] = 'Pittsburgh Penguins'
clubDictNHL['SJS'] = 'San Jose Sharks'
clubDictNHL['STL'] = 'St. Louis Blues'
clubDictNHL['TBL'] = 'Tampa Bay Lightning'
clubDictNHL['TOR'] = 'Toronto Maple Leafs'
clubDictNHL['VAN'] = 'Vancouver Canucks'
clubDictNHL['WPG'] = 'Winnipeg Jets'
clubDictNHL['WSH'] = 'Washington Capitals'

# NBA CLUBS DICT
clubDictNBA        = dict()
clubDictNBA['ATL'] = 'Atlanta Hawks'
clubDictNBA['BOS'] = 'Boston Celtics'
clubDictNBA['BRO'] = 'Brooklyn Nets'
clubDictNBA['CHA'] = 'Charlotte Hornets'
clubDictNBA['CHI'] = 'Chicago Bulls'
clubDictNBA['CLE'] = 'Cleveland Cavaliers'
clubDictNBA['DAL'] = 'Dallas Mavericks'
clubDictNBA['DEN'] = 'Denver Nuggets'
clubDictNBA['DET'] = 'Detroit Pistons'
clubDictNBA['GSW'] = 'Golden State Warriors'
clubDictNBA['HOU'] = 'Houston Rockets'
clubDictNBA['IND'] = 'Indiana Pacers'
clubDictNBA['LAC'] = 'Los Angeles Clippers'
clubDictNBA['LAK'] = 'Los Angeles Lakers'
clubDictNBA['MEM'] = 'Memphis Grizzlies'
clubDictNBA['MIA'] = 'Miami Heat'
clubDictNBA['MIN'] = 'Minnesota Timberwolves'
clubDictNBA['MIL'] = 'Milwaukee Bucks'
clubDictNBA['NOR'] = 'New Orleans Pelicans'
clubDictNBA['NYK'] = 'New York Knicks'
clubDictNBA['OKC'] = 'Oklahoma City Thunder'
clubDictNBA['ORL'] = 'Orlando Magic'
clubDictNBA['PHI'] = 'Philadelphia 76ers'
clubDictNBA['PHO'] = 'Phoenix Suns'
clubDictNBA['POR'] = 'Portland Trail Blazers'
clubDictNBA['SAC'] = 'Sacramento Kings'
clubDictNBA['SAS'] = 'San Antonio Spurs'
clubDictNBA['TOR'] = 'Toronto Raptors'
clubDictNBA['UTA'] = 'Utah Jazz'
clubDictNBA['WAS'] = 'Washington Wizards'

# DICT OF CLUB DICTS
clubs        = dict()
clubs['NHL'] = clubDictNHL
clubs['NBA'] = clubDictNBA


# 26 RGB colors
rgb26 = [
    (2, 63, 165),
    (125, 135, 185),
    (190, 193, 212),
    (214, 188, 192),
    (187, 119, 132),
    (142, 6, 59),
    (74, 111, 227),
    (133, 149, 225),
    (181, 187, 227),
    (230, 175, 185),
    (224, 123, 145),
    (211, 63, 106),
    (17, 198, 56),
    (141, 213, 147),
    (198, 222, 199),
    (234, 211, 198),
    (240, 185, 141),
    (239, 151, 8),
    (15, 207, 192),
    (156, 222, 214),
    (213, 234, 231),
    (243, 225, 235),
    (246, 196, 225),
    (247, 156, 212)
]
