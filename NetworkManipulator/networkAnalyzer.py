__author__ = '3buson'

import networkBuilder

def createAndAnalyzeNetwork(leagueId, seasonId):
    return ''

def main():
    leagueId = 1

    seasonsInput = raw_input('Please enter desired seasons separated by comma (all for all of them): ')

    if(seasonsInput.lower() == 'all'):
        seasons = seasonsInput
    else:
        seasons = seasonsInput.split(',')
        seasons = [int(season) for season in seasons]

    for season in seasons:
        clubsNetwork = networkBuilder.buildNetwork(leagueId, season)

        # TODO: analyze network


if __name__ == "__main__":
    main()
