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
allSeasons          = range(1976,2015)
allLeagues          = range(1,3)

# --- DATABASE --- #
databaseString = 'DRIVER=(MySQL);SERVER=localhost;DATABASE=sportnetwork;UID=root;PWD=*****'

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
leagues['NBA'] = 'National Basketball Association'
leagues['NHL'] = 'National Hockey League'

# --- CLUBS DICTS --- #

# NHL CLUBS DICT
clubDictNHL        = dict()
clubDictNHL['ANA'] = 'Anaheim Ducks'
clubDictNHL['ARI'] = 'Arizona Coyotes'
clubDictNHL['BOS'] = 'Boston Bruins'
clubDictNHL['BUF'] = 'Buffalo Sabres'
clubDictNHL['CAR'] = 'Carolina Huricanes'
clubDictNHL['CBJ'] = 'Columbus Blue Jackets'
clubDictNHL['CGY'] = 'Calgary Flames'
clubDictNHL['CHI'] = 'Chicago Blackhawks'
clubDictNHL['COL'] = 'Colorado Avalanche'
clubDictNHL['DAL'] = 'Dallas Stars'
clubDictNHL['DET'] = 'Detroit Red Wings'
clubDictNHL['EDM'] = 'Edmonton Oilers'
clubDictNHL['FLA'] = 'Florida Panthers'
clubDictNHL['LAK'] = 'Los Angeles Kings'
clubDictNHL['MIN'] = 'Minesotta Wild'
clubDictNHL['MTL'] = 'Montreal Canadiens'
clubDictNHL['NJD'] = 'New Jersey Devils'
clubDictNHL['NSH'] = 'Nashville Predators'
clubDictNHL['NYI'] = 'New York Islanders'
clubDictNHL['NYR'] = 'New York Rangers'
clubDictNHL['OTT'] = 'Ottawa Senators'
clubDictNHL['PHI'] = 'Philadelphia Flyers'
clubDictNHL['PIT'] = 'Pittsburg Penguins'
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
