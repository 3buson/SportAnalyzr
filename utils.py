__author__ = '3buson'

import time
import numpy
import pyodbc
import traceback
import networkx as nx
from datetime import date
from collections import deque
from matplotlib import pyplot

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


def creteGraph(xs, ys, ysMin, ysMax, style='b-', logScale=False, title=None, xLabel=None, yLabel=None, filename=None):
    pyplot.figure(0)

    if (logScale):
        pyplot.loglog(ys, style)
    else:
        pyplot.ylim([ysMin, ysMax])
        pyplot.plot(xs, ys, style)


    if (title):
        pyplot.title(title)

    if xLabel:
        pyplot.xlabel(xLabel)

    if yLabel:
        pyplot.ylabel(yLabel)

    if filename:
        pyplot.savefig(filename)
    else:
        pyplot.show()

    pyplot.close()

def createMultiGraph(ysMin=None, ysMax=None, logScale=False, title=None, xLabel=None, yLabel=None, filename=None, xs=None, ysFirst=None, ysSecond=None, ysThird=None):
    pyplot.figure(0)

    if (logScale):
        if (ysFirst):
            pyplot.loglog(ysFirst,  'b-')
        if (ysSecond):
            pyplot.loglog(ysSecond, 'r-')
        if (ysThird):
            pyplot.loglog(ysThird,  'k-')
    else:
        if (ysMin and ysMax):
            pyplot.ylim([ysMin, ysMax])

        if (ysFirst):
            pyplot.plot(xs, ysSecond, 'r-')
        if (ysSecond):
            pyplot.plot(xs, ysFirst,  'b-')
        if (ysThird):
            pyplot.plot(xs, ysThird,  'k-')


    if (title):
        pyplot.title(title)

    if xLabel:
        pyplot.xlabel(xLabel)

    if yLabel:
        pyplot.ylabel(yLabel)

    if filename:
        pyplot.savefig(filename)
    else:
        pyplot.show()

    pyplot.close()

def getCDFYValuesFromDict(input):
    sortedValues = sorted(input.values())

    return numpy.arange(len(sortedValues)) / float(len(sortedValues) - 1)

def createCDFGraph(input, title=None, xLabel=None, yLabel=None, filename=None):
    pyplot.figure(0)

    pyplot.plot(sorted(input.values()), getCDFYValuesFromDict(input))

    if (title):
        pyplot.title(title)

    if xLabel:
        pyplot.xlabel(xLabel)

    if yLabel:
        pyplot.ylabel(yLabel)

    if filename:
        pyplot.savefig(filename)
    else:
        pyplot.show()

    pyplot.close()
