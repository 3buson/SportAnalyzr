import os
import time
import urlgrabber

import constants


__author__ = '3buson'

baseDirname = 'html/'


def fetchHTMLFiles(clubDict, league, season='2016'):
    # create csv directory
    dir = os.path.dirname(baseDirname)
    if not os.path.exists(dir):
        os.makedirs(dir)

    # create league directory inside HTML directory
    dir = os.path.dirname(baseDirname + league + '/')
    if not os.path.exists(dir):
        os.makedirs(dir)

    # create season directory inside league directory
    dir = os.path.dirname(baseDirname + league + '/' + season + '/')
    if not os.path.exists(dir):
        os.makedirs(dir)

    print "[File Conqueror]  Getting HTML for league: %s\tseason: %s" % (league, season)

    url = constants.urls[league]['baseUrl'] + constants.urls[league]['urlPrefix'] + season + constants.urls[league]['urlSuffix']

    filename = baseDirname + league + '/' + season + '/' + 'playerStats.html'

    try:
        urlgrabber.urlgrab(url, filename, retries=5)
    except Exception, e:
        time.sleep(60)
        urlgrabber.urlgrab(url, filename, retries=5)

        print "Exception occurred!", e
        print "URL: ", url

        pass

def main():
    for season in constants.seasons.keys():
        for league in constants.leagues.keys():
            fetchHTMLFiles(constants.clubs[league], league, season)

        print "\n[File Conqueror]  Fetched HTML files for all leagues for season %s\n" % season


if __name__ == "__main__":
    main()
