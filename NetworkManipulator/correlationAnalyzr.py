import math
import scipy.stats
from random import randint


__author__ = '3buson'


def calculateCorrelation(input1, input2, correlationType='pearson'):
    if correlationType == 'pearson':
        rho, p = scipy.stats.pearsonr(input1, input2)
    else:
        rho, p = scipy.stats.spearmanr(input1, input2)

    return rho, p


def bootstrapCorrelation(input1, input2, correlationType='pearson', confidenceInterval=95, bootstrapSamples=1000):
    # bootstrap
    input1Samples = []
    input2Samples = []
    for i in range(0, bootstrapSamples):
        input1Sample = []
        input2Sample = []

        for j in range(0, len(input1)):
            randomIndex = randint(0, len(input1) - 1)

            input1Sample.append(input1[randomIndex])
            input2Sample.append(input2[randomIndex])

        input1Samples.append(input1Sample)
        input2Samples.append(input2Sample)

    correlations = []
    for i in range(0, len(input1Samples)):
        if correlationType == 'pearson':
            rho, p = scipy.stats.pearsonr(input1Samples[i], input2Samples[i])
        else:
            rho, p = scipy.stats.spearmanr(input1Samples[i], input2Samples[i])

        correlations.append(rho)

    correlations.sort()

    lowerIndex = int(math.floor(bootstrapSamples * ((100 - confidenceInterval) / 2) / 100.0))
    upperIndex = int(math.floor(bootstrapSamples * (confidenceInterval + (100 - confidenceInterval) / 2) / 100.0))

    lower = correlations[lowerIndex]
    upper = correlations[upperIndex]

    return lower, upper
