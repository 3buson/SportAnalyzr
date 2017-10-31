import time
import pyodbc
import warnings
import traceback


__author__ = '3buson'


mode = 'normal'


### --- DATABASE FUNCTIONS --- ###

def connectToDB():
    connection = None

    while connection is None:
        try:
            connection = pyodbc.connect('DSN=SportAnalyzr2')

        except Exception, e:
            print "\n[DB connector]  Error connecting to database. Trying again in 1 sec.", e
            traceback.print_exc()

        time.sleep(1)

    return connection


def ignoreWarnings():
    warnings.simplefilter("ignore")
