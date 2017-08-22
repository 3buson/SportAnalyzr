import os
import csv
import time
import math
import scipy

import constants

from Visualizer import visualizer


__author__ = '3buson'


def calculateCorrelation(input1, input2, correlationType='pearson'):
    if correlationType == 'pearson':
        rho, p = scipy.stats.pearsonr(input1, input2)
    else:
        rho, p = scipy.stats.spearmanr(input1, input2)

    return rho
