__author__ = '3buson'

import time
import numpy
import pyodbc
import traceback

from operator import add
from operator import sub
from matplotlib import pyplot
from scipy.stats import norm

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


def createGraph(xs, ys, xsMin, xsMax, ysMin, ysMax, style='b-', logScale=False, title=None, xLabel=None, yLabel=None, filename=None):
    pyplot.figure(0)

    if logScale:
        pyplot.loglog(ys, style)
    else:
        pyplot.ylim([ysMin, ysMax])
        pyplot.plot(xs, ys, style)

    if xsMin is not None and xsMax is not None:
        pyplot.xlim([xsMin, xsMax])

    if title:
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


def createMultiGraph(ysMin=None, ysMax=None, logScale=False, title=None, xLabel=None, yLabel=None, filename=None, xs=None, ysDoubleArray=None, colors=['b', 'k', 'r', 'm', 'g'], labels=None):
    pyplot.figure(0)

    for idx, ys in enumerate(ysDoubleArray):
        if logScale:
            pyplot.loglog(xs, ys, colors[idx] + '-')
        else:
            if labels is not None:
                label = labels[idx]
            else:
                label = None

            pyplot.plot(xs, ys, colors[idx] + '-', label=label)

    pyplot.legend(loc='best')

    if title:
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


def createDoubleGraphWithVariance(ysMin=None, ysMax=None, title=None, xLabel=None, yLabel=None, filename=None, xs=None, ys1=None, ys2=None, ys1Deviation=None, ys2Deviation=None, labels=None):
    pyplot.figure(0)

    if ysMin is not None and ysMax is not None:
        pyplot.ylim([ysMin, ysMax])

    if ys1:
        if labels is not None:
            label = labels[0]
        else:
            label = None

        pyplot.plot(xs, ys1, 'b-', label=label)

    if ys1Deviation:
        deviationUp   = map(add, ys1, ys1Deviation)
        deviationDown = map(sub, ys1, ys1Deviation)

        pyplot.plot(xs, deviationUp,   'b--')
        pyplot.plot(xs, deviationDown, 'b--')

    if ys2:
        if labels is not None:
            label = labels[0]
        else:
            label = None

        pyplot.plot(xs, ys2, 'r-', label=label)

    if ys2Deviation:
        deviationUp   = map(add, ys2, ys2Deviation)
        deviationDown = map(sub, ys2, ys2Deviation)

        pyplot.plot(xs, deviationUp,   'r--')
        pyplot.plot(xs, deviationDown, 'r--')

    pyplot.legend(loc='best')

    if title:
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


def createMultiGraphWithVariance(ysMin=None, ysMax=None, title=None, xLabel=None, yLabel=None, filename=None, xs=None, ysDoubleArray=None, ysDeviationDoubleArray=None, colors=['b', 'k', 'r', 'm', 'g'], labels=None):
    pyplot.figure(0)

    if ysMin is not None and ysMax is not None:
        pyplot.ylim([ysMin, ysMax])

    for idx, ys in enumerate(ysDoubleArray):
        if labels is not None:
            label = labels[idx]
        else:
            label = None

        pyplot.plot(xs, ys, colors[idx] + '-', label=label)

    for idx, ysDeviation in enumerate(ysDeviationDoubleArray):
        deviationUp   = map(add, ysDoubleArray[idx], ysDeviation)
        deviationDown = map(sub, ysDoubleArray[idx], ysDeviation)

        pyplot.plot(xs, deviationUp,   colors[idx] + '--')
        pyplot.plot(xs, deviationDown, colors[idx] + '--')

    pyplot.legend(loc='best')

    if title:
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


def createCDFGraph(input, xsMin, xsMax, title=None, xLabel=None, yLabel=None, filename=None, style='b-'):
    pyplot.figure(0)

    if xsMin is not None and xsMax is not None:
        pyplot.xlim([xsMin, xsMax])

    if title:
        pyplot.title(title)

    if xLabel:
        pyplot.xlabel(xLabel)

    if yLabel:
        pyplot.ylabel(yLabel)

    pyplot.plot(sorted(input.values()), getCDFYValuesFromDict(input), style)

    if filename:
        pyplot.savefig(filename)
    else:
        pyplot.show()

    pyplot.close()


def getPDFYValuesFromDict(input, numberOfBins=12):
    sortedValues = sorted(input.values())

    p, x = numpy.histogram(sortedValues, numberOfBins)
    x = x[:-1] + (x[1] - x[0]) / 2           # convert bin edges to centers
    p = [float(prob) / sum(p) for prob in p] # divide every element by sum to get [0,1) range

    return x.tolist(), p


def createPDFGraph(input, xsMin, xsMax, title=None, xLabel=None, yLabel=None, filename=None, color='b', numberOfBins=12):
    pyplot.figure(0)

    if xsMin is not None and xsMax is not None:
        pyplot.xlim([xsMin, xsMax])

    pyplot.ylim([0, 1])

    if title:
        pyplot.title(title)

    if xLabel:
        pyplot.xlabel(xLabel)

    if yLabel:
        pyplot.ylabel(yLabel)

    x, p = getPDFYValuesFromDict(input, numberOfBins)

    pyplot.bar(x, p, color=color)

    if filename:
        pyplot.savefig(filename)
    else:
        pyplot.show()

    pyplot.close()
