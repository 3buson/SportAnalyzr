import os
import csv

import utils
import sportAnalyzr
import NetworkManipulator.correlationAnalyzr
from NetworkManipulator import correlationAnalyzr

__author__ = '3buson'

def main():
    for league in ['Italy Serie A', 'Spain LaLiga', 'England Premier League', 'Germany 1. Bundesliga', 'France Ligue 1', 'Portugal Liga NOS', 'Scotland Premier League', 'Netherlands Eredevisie']:
        attendance_csv = 'FileConqueror/csv/attendance/' + league + ' attendance.csv'
        properties_csv = 'output/' + league + ' NetworkPropertiesOverTimeRegular.csv'

        attendance_array = []
        pr_rel_entropy_array = []

        rownum = 0
        with open(attendance_csv, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                # skip header
                if rownum == 0:
                    rownum += 1
                else:
                    season = int(row[0])

                    if season > 1999 and season < 2015:
                        attendance_array.append(float(row[1]))

        with open(properties_csv, 'rb') as f:
            reader = csv.reader(f, delimiter=',')

            for row in reader:
                if row[0] == 'pageRankRelativeEntropy':
                    pr_rel_entropy_array = [float(res) for res in row[5].split(' ')]

        if len(attendance_array) == len(pr_rel_entropy_array):
            pearson = correlationAnalyzr.calculateCorrelation(attendance_array, pr_rel_entropy_array, 'pearson')
            spearman = correlationAnalyzr.calculateCorrelation(attendance_array, pr_rel_entropy_array, 'spearman')

            print "\n[Correlation Tester]:  Correlation for league %s: Pearson: %f, Spearman: %f" % (league, pearson, spearman)
        else:
            print "\n[Correlation Tester]:  Error! Arrays do not match for league %s. Length %d, %d" % (league, len(attendance_array), len(pr_rel_entropy_array))

if __name__ == "__main__":
    main()
