__author__ = '3buson'

import time
import pyodbc
import traceback
import networkx as nx
from datetime import date
from collections import deque

import constants


### ---- DATABASE FUNCTIONS ---- ###

def connectToDB():
    connection = None

    while connection is None:
        try:
            connection = pyodbc.connect('DSN=SportAnalyzr')

        except Exception, e:
            print "\n[DB connector]  Error connecting to database. Trying again in 1 sec.", e
            traceback.print_exc()

        time.sleep(1)

    return connection
