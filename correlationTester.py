import os
import csv

import constants

import numpy
from Visualizer import visualizer
from NetworkManipulator import correlationAnalyzr

__author__ = '3buson'

def correlationOfUniformityAndBetsPerGame(confidenceInterval, bootstrapSamples):
    bets_uniformity_per_game_csv = 'FileConqueror/csv/bets/volume_uniformity_per_game.csv'

    correlation_dict = dict()

    correlation_arrays_uniformity_combined = []
    correlation_arrays_betsVolume_combined = []

    rownum = 0
    if os.path.isfile(bets_uniformity_per_game_csv):
        with open(bets_uniformity_per_game_csv, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                # skip header
                if rownum == 0:
                    rownum += 1
                else:
                    league = row[0]
                    uniformity = float(row[1])
                    betsVolume = float(row[2])

                    if league in correlation_dict.keys():
                        correlation_dict[league]['uniformity'].append(uniformity)
                        correlation_dict[league]['betsVolume'].append(betsVolume)
                    else:
                        correlation_dict[league] = {
                            'uniformity': [uniformity],
                            'betsVolume': [betsVolume]
                        }

    for league, correlation_arrays in correlation_dict.iteritems():
        uniformities = correlation_arrays['uniformity']
        betsVolumes = correlation_arrays['betsVolume']

        [pearson, pp] = correlationAnalyzr.calculateCorrelation(uniformities, betsVolumes, 'pearson')
        [spearman, sp] = correlationAnalyzr.calculateCorrelation(uniformities, betsVolumes, 'spearman')

        [pLower, pUpper] = correlationAnalyzr.bootstrapCorrelation(uniformities, betsVolumes, 'pearson', confidenceInterval, bootstrapSamples)
        [sLower, sUpper] = correlationAnalyzr.bootstrapCorrelation(uniformities, betsVolumes, 'spearman', confidenceInterval, bootstrapSamples)

        correlation_arrays_uniformity_combined = correlation_arrays_uniformity_combined + uniformities
        correlation_arrays_betsVolume_combined = correlation_arrays_betsVolume_combined + betsVolumes

        print "[Correlation Tester]:  Bets Volume and Uniformity correlation for league %s:" \
              "\n\tPearson: %f, p: %f" \
              "\n\t%d samples for confidence interval %d%%: [%f, %f] " \
              "\n\tSpearman: %f, p: %f" \
              "\n\t%d samples for confidence interval %d%%: [%f, %f] " % \
              (league, pearson, pp, bootstrapSamples, confidenceInterval, pLower, pUpper, spearman, sp, bootstrapSamples, confidenceInterval, sLower, sUpper)

    print ""

    [pearson, pp] = correlationAnalyzr.calculateCorrelation(correlation_arrays_uniformity_combined, correlation_arrays_betsVolume_combined, 'pearson')
    [spearman, sp] = correlationAnalyzr.calculateCorrelation(correlation_arrays_uniformity_combined, correlation_arrays_betsVolume_combined, 'spearman')

    [pLower, pUpper] = correlationAnalyzr.bootstrapCorrelation(correlation_arrays_uniformity_combined, correlation_arrays_betsVolume_combined, 'pearson', confidenceInterval, bootstrapSamples)
    [sLower, sUpper] = correlationAnalyzr.bootstrapCorrelation(correlation_arrays_uniformity_combined, correlation_arrays_betsVolume_combined, 'spearman', confidenceInterval, bootstrapSamples)

    print "[Correlation Tester]:  Bets Volume and Uniformity correlation for all leagues combined:" \
          "\n\tPearson: %f, p: %f" \
          "\n\t%d samples for confidence interval %d%%: [%f, %f] " \
          "\n\tSpearman: %f, p: %f" \
          "\n\t%d samples for confidence interval %d%%: [%f, %f] " % \
          (pearson, pp, bootstrapSamples, confidenceInterval, pLower, pUpper, spearman, sp, bootstrapSamples,
           confidenceInterval, sLower, sUpper)

    print ""
    print "-------------------------------------------------------------------------------------------------"


def main():
    leagues = [
        'National Basketball Association',
        'Italy Serie A',
        'Spain LaLiga',
        'England Premier League',
        'Germany 1. Bundesliga',
        'France Ligue 1',
        'Scotland Premier League',
        'Netherlands Eredevisie',
        'Portugal Liga NOS'
    ]

    confidenceInterval = 95
    bootstrapSamples = 1000

    correlationOfUniformityAndBetsPerGame(confidenceInterval, bootstrapSamples)

    attendanceCorrelationsDictionary = dict()
    betsCorrelationsDictionary = dict()
    leagueValueCorrelationsDictionary = dict()

    combined_attendance_array = []
    combined_pr_rel_entropy_array = []

    for league in leagues:
        bets_csv       = 'FileConqueror/csv/bets/' + league + ' bets volume.csv'
        value_csv      = 'FileConqueror/csv/league_value/' + league + ' value.csv'
        attendance_csv = 'FileConqueror/csv/attendance/' + league + ' attendance.csv'
        properties_csv = 'output/' + league + ' NetworkPropertiesOverTimeRegular.csv'

        bets_array = []
        value_array = []
        attendance_array = []
        pr_rel_entropy_array = []

        if league == 'National Basketball Association':
            properties_csv_all = 'output/' + league + ' NetworkPropertiesOverTimeAll.csv'
            properties_csv_playoff = 'output/' + league + ' NetworkPropertiesOverTimePlayoff.csv'

            pr_rel_entropy_array_all = []
            pr_rel_entropy_array_playoff = []

            rownum = 0
            if os.path.isfile(attendance_csv):
                with open(attendance_csv, 'rb') as f:
                    reader = csv.reader(f, delimiter=',')
                    for row in reader:
                        # skip header
                        if rownum == 0:
                            rownum += 1
                        else:
                            season = int(row[0])

                            if season > 1975 and season < 2015:
                                attendance_array.append(float(row[1]))
            else:
                attendance_array = []

            # inverted - most recent season is first
            attendance_array.reverse()

            attendance_array_string = ', '.join([str(v) for v in attendance_array])

            # print "[Correlation Tester]:  Attendance array for league %s: %s" % (league, attendance_array_string)

            rownum = 0
            if os.path.isfile(bets_csv):
                with open(bets_csv, 'rb') as f:
                    reader = csv.reader(f, delimiter=',')
                    for row in reader:
                        # skip header
                        if rownum == 0:
                            rownum += 1
                        else:
                            season = int(row[0])

                            if season > 1999 and season < 2015:
                                bets_array.append(float(row[1]))
            else:
                bets_array = []

            bets_array_string = ', '.join([str(v) for v in bets_array])

            # print "[Correlation Tester]:  Bets volume array for league %s: %s" % (league, bets_array_string)

            with open(properties_csv, 'rb') as f:
                reader = csv.reader(f, delimiter=',')

                for row in reader:
                    if row[0] == 'pageRankRelativeEntropy':
                        pr_rel_entropy_array = [float(res) for res in row[5].split(' ')]

            with open(properties_csv_all, 'rb') as f:
                reader = csv.reader(f, delimiter=',')

                for row in reader:
                    if row[0] == 'pageRankRelativeEntropy':
                        pr_rel_entropy_array_all = [float(res) for res in row[5].split(' ')]

            with open(properties_csv_playoff, 'rb') as f:
                reader = csv.reader(f, delimiter=',')

                for row in reader:
                    if row[0] == 'pageRankRelativeEntropy':
                        pr_rel_entropy_array_playoff = [float(res) for res in row[5].split(' ')]

            if len(attendance_array) == len(pr_rel_entropy_array):
                [pearson, pp] = correlationAnalyzr.calculateCorrelation(attendance_array, pr_rel_entropy_array, 'pearson')
                [spearman, sp] = correlationAnalyzr.calculateCorrelation(attendance_array, pr_rel_entropy_array, 'spearman')

                [pLower, pUpper] = correlationAnalyzr.bootstrapCorrelation(attendance_array, pr_rel_entropy_array, 'pearson', confidenceInterval, bootstrapSamples)
                [sLower, sUpper] = correlationAnalyzr.bootstrapCorrelation(attendance_array, pr_rel_entropy_array, 'spearman', confidenceInterval, bootstrapSamples)

                attendanceCorrelationsDictionary[league] = {
                    'pearson': pearson,
                    'pearsonLower': pLower,
                    'pearsonUpper': pUpper,
                    'spearman': spearman,
                    'spearmanLower': sLower,
                    'spearmanUpper': sUpper
                }

                print "[Correlation Tester]:  Attendance correlation for league %s REGULAR:" \
                      "\n\tPearson: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " \
                      "\n\tSpearman: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " % \
                      (league, pearson, pp, bootstrapSamples, confidenceInterval, pLower, pUpper, spearman, sp, bootstrapSamples, confidenceInterval, sLower, sUpper)

                avg_attendance = float(sum(attendance_array)) / max(len(attendance_array), 1)
                std_dev_attendance = numpy.std(attendance_array, ddof=1)

                combined_attendance_array += [((a - avg_attendance) / std_dev_attendance) for a in attendance_array]
                combined_pr_rel_entropy_array += pr_rel_entropy_array
            else:
                print "[Correlation Tester]:  Error! Arrays do not match for league %s REGULAR. Length %d, %d" % (league, len(attendance_array), len(pr_rel_entropy_array))

            if len(attendance_array) == len(pr_rel_entropy_array_all):
                [pearson, pp] = correlationAnalyzr.calculateCorrelation(attendance_array, pr_rel_entropy_array_all, 'pearson')
                [spearman, sp] = correlationAnalyzr.calculateCorrelation(attendance_array, pr_rel_entropy_array_all, 'spearman')

                [pLower, pUpper] = correlationAnalyzr.bootstrapCorrelation(attendance_array, pr_rel_entropy_array_all, 'pearson', confidenceInterval, bootstrapSamples)
                [sLower, sUpper] = correlationAnalyzr.bootstrapCorrelation(attendance_array, pr_rel_entropy_array_all, 'spearman', confidenceInterval, bootstrapSamples)

                print "[Correlation Tester]:  Attendance correlation for league %s ALL:" \
                      "\n\tPearson: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " \
                      "\n\tSpearman: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " % \
                      (league, pearson, pp, bootstrapSamples, confidenceInterval, pLower, pUpper, spearman, sp, bootstrapSamples, confidenceInterval, sLower, sUpper)
            else:
                print "[Correlation Tester]:  Error! Arrays do not match for league %s ALL. Length %d, %d" % (league, len(attendance_array), len(pr_rel_entropy_array_all))

            if len(attendance_array) == len(pr_rel_entropy_array_playoff):
                [pearson, pp] = correlationAnalyzr.calculateCorrelation(attendance_array, pr_rel_entropy_array_playoff, 'pearson')
                [spearman, sp] = correlationAnalyzr.calculateCorrelation(attendance_array, pr_rel_entropy_array_playoff, 'spearman')

                [pLower, pUpper] = correlationAnalyzr.bootstrapCorrelation(attendance_array, pr_rel_entropy_array_playoff, 'pearson', confidenceInterval, bootstrapSamples)
                [sLower, sUpper] = correlationAnalyzr.bootstrapCorrelation(attendance_array, pr_rel_entropy_array_playoff, 'spearman', confidenceInterval, bootstrapSamples)

                print "[Correlation Tester]:  Attendance correlation for league %s PLAYOFF:" \
                      "\n\tPearson: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " \
                      "\n\tSpearman: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " % \
                      (league, pearson, pp, bootstrapSamples, confidenceInterval, pLower, pUpper, spearman, sp, bootstrapSamples, confidenceInterval, sLower, sUpper)
            else:
                print "[Correlation Tester]:  Error! Arrays do not match for league %s PLAYOFF. Length %d, %d" % (league, len(attendance_array), len(pr_rel_entropy_array_playoff))

            pr_rel_entropy_array_reduced = pr_rel_entropy_array[29:38]
            if len(bets_array) == len(pr_rel_entropy_array_reduced):
                [pearson, pp] = correlationAnalyzr.calculateCorrelation(bets_array, pr_rel_entropy_array_reduced, 'pearson')
                [spearman, sp] = correlationAnalyzr.calculateCorrelation(bets_array, pr_rel_entropy_array_reduced, 'spearman')

                [pLower, pUpper] = correlationAnalyzr.bootstrapCorrelation(bets_array, pr_rel_entropy_array_reduced, 'pearson', confidenceInterval, bootstrapSamples)
                [sLower, sUpper] = correlationAnalyzr.bootstrapCorrelation(bets_array, pr_rel_entropy_array_reduced, 'spearman', confidenceInterval, bootstrapSamples)

                betsCorrelationsDictionary[league] = {
                    'pearson': pearson,
                    'pearsonLower': pLower,
                    'pearsonUpper': pUpper,
                    'spearman': spearman,
                    'spearmanLower': sLower,
                    'spearmanUpper': sUpper
                }

                print "[Correlation Tester]:  Bets volume correlation for league %s:" \
                      "\n\tPearson: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " \
                      "\n\tSpearman: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " % \
                      (league, pearson, pp, bootstrapSamples, confidenceInterval, pLower, pUpper, spearman, sp, bootstrapSamples, confidenceInterval, sLower, sUpper)
            else:
                print "[Correlation Tester]:  Error! Arrays do not match for league %s. Length %d, %d" % (
                league, len(bets_array), len(pr_rel_entropy_array_reduced))

            print ""
            print "-------------------------------------------------------------------------------------------------"
        else:
            rownum = 0
            if os.path.isfile(value_csv):
                with open(value_csv, 'rb') as f:
                    reader = csv.reader(f, delimiter=',')
                    for row in reader:
                        # skip header
                        if rownum == 0:
                            rownum += 1
                        else:
                            season = int(row[0])

                            if season > 1999 and season < 2016:
                                inflationRatio = constants.inflationRatio / 100  # average inflation ratio per year (percent)
                                valueInflationRatio = 1 + ((2016 - season) * inflationRatio)

                                value_array.append(float(row[1]) * valueInflationRatio)
            else:
                value_array = []

            # inverted - most recent season is first
            value_array.reverse()

            value_array_string = ', '.join([str(v) for v in value_array])

            # print "[Correlation Tester]:  League value array for league %s: %s" % (league, value_array_string)


            rownum = 0
            if os.path.isfile(attendance_csv):
                with open(attendance_csv, 'rb') as f:
                    reader = csv.reader(f, delimiter=',')
                    for row in reader:
                        # skip header
                        if rownum == 0:
                            rownum += 1
                        else:
                            season = int(row[0])

                            if season > 1999 and season < 2016:
                                attendance_array.append(float(row[1]))
            else:
                attendance_array = []

            # inverted - most recent season is first
            attendance_array.reverse()

            attendance_array_string = ', '.join([str(v) for v in attendance_array])

            # print "[Correlation Tester]:  Attendance array for league %s: %s" % (league, attendance_array_string)

            rownum = 0
            if os.path.isfile(bets_csv):
                with open(bets_csv, 'rb') as f:
                    reader = csv.reader(f, delimiter=',')
                    for row in reader:
                        # skip header
                        if rownum == 0:
                            rownum += 1
                        else:
                            season = int(row[0])

                            if season > 1999 and season < 2015:
                                bets_array.append(float(row[1]))
            else:
                bets_array = []

            bets_array_string = ', '.join([str(v) for v in bets_array])

            # print "[Correlation Tester]:  Bets volume array for league %s: %s" % (league, bets_array_string)


            with open(properties_csv, 'rb') as f:
                reader = csv.reader(f, delimiter=',')

                for row in reader:
                    if row[0] == 'pageRankRelativeEntropy':
                        pr_rel_entropy_array = [float(res) for res in row[5].split(' ')]

            pr_rel_entropy_array_reduced = pr_rel_entropy_array[4:15]
            if len(value_array) == len(pr_rel_entropy_array_reduced):
                [pearson,  pp] = correlationAnalyzr.calculateCorrelation(value_array, pr_rel_entropy_array_reduced , 'pearson')
                [spearman, sp] = correlationAnalyzr.calculateCorrelation(value_array, pr_rel_entropy_array_reduced , 'spearman')

                [pLower, pUpper] = correlationAnalyzr.bootstrapCorrelation(value_array, pr_rel_entropy_array_reduced, 'pearson', confidenceInterval, bootstrapSamples)
                [sLower, sUpper] = correlationAnalyzr.bootstrapCorrelation(value_array, pr_rel_entropy_array_reduced, 'spearman', confidenceInterval, bootstrapSamples)

                leagueValueCorrelationsDictionary[league] = {
                    'pearson': pearson,
                    'pearsonLower': pLower,
                    'pearsonUpper': pUpper,
                    'spearman': spearman,
                    'spearmanLower': sLower,
                    'spearmanUpper': sUpper
                }

                print "[Correlation Tester]:  League value correlation for league %s:" \
                      "\n\tPearson: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " \
                      "\n\tSpearman: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " % \
                      (league, pearson, pp, bootstrapSamples, confidenceInterval, pLower, pUpper, spearman, sp, bootstrapSamples, confidenceInterval, sLower, sUpper)
            else:
                print "[Correlation Tester]:  Error! Arrays do not match for league %s. Length %d, %d" % (league, len(value_array), len(pr_rel_entropy_array_reduced))

            if len(attendance_array) == len(pr_rel_entropy_array):
                [pearson,  pp] = correlationAnalyzr.calculateCorrelation(attendance_array, pr_rel_entropy_array, 'pearson')
                [spearman, sp] = correlationAnalyzr.calculateCorrelation(attendance_array, pr_rel_entropy_array, 'spearman')

                [pLower, pUpper] = correlationAnalyzr.bootstrapCorrelation(attendance_array, pr_rel_entropy_array, 'pearson', confidenceInterval, bootstrapSamples)
                [sLower, sUpper] = correlationAnalyzr.bootstrapCorrelation(attendance_array, pr_rel_entropy_array, 'spearman', confidenceInterval, bootstrapSamples)

                attendanceCorrelationsDictionary[league] = {
                    'pearson': pearson,
                    'pearsonLower': pLower,
                    'pearsonUpper': pUpper,
                    'spearman': spearman,
                    'spearmanLower': sLower,
                    'spearmanUpper': sUpper
                }

                print "[Correlation Tester]:  Attendance correlation for league %s:" \
                      "\n\tPearson: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " \
                      "\n\tSpearman: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " % \
                      (league, pearson, pp, bootstrapSamples, confidenceInterval, pLower, pUpper, spearman, sp, bootstrapSamples, confidenceInterval, sLower, sUpper)

                avg_attendance = float(sum(attendance_array)) / max(len(attendance_array), 1)
                std_dev_attendance = numpy.std(attendance_array, ddof=1)

                combined_attendance_array += [((a - avg_attendance) / std_dev_attendance) for a in attendance_array]
                combined_pr_rel_entropy_array += pr_rel_entropy_array
            else:
                print "[Correlation Tester]:  Error! Arrays do not match for league %s. Length %d, %d" % (league, len(attendance_array), len(pr_rel_entropy_array))

            pr_rel_entropy_array_reduced = pr_rel_entropy_array[5:14]
            if len(bets_array) == len(pr_rel_entropy_array_reduced):
                [pearson,  pp] = correlationAnalyzr.calculateCorrelation(bets_array, pr_rel_entropy_array_reduced, 'pearson')
                [spearman, sp] = correlationAnalyzr.calculateCorrelation(bets_array, pr_rel_entropy_array_reduced, 'spearman')

                [pLower, pUpper] = correlationAnalyzr.bootstrapCorrelation(bets_array, pr_rel_entropy_array_reduced, 'pearson', confidenceInterval, bootstrapSamples)
                [sLower, sUpper] = correlationAnalyzr.bootstrapCorrelation(bets_array, pr_rel_entropy_array_reduced, 'spearman', confidenceInterval, bootstrapSamples)

                betsCorrelationsDictionary[league] = {
                    'pearson': pearson,
                    'pearsonLower': pLower,
                    'pearsonUpper': pUpper,
                    'spearman': spearman,
                    'spearmanLower': sLower,
                    'spearmanUpper': sUpper
                }

                print "[Correlation Tester]:  Bets volume correlation for league %s:" \
                      "\n\tPearson: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " \
                      "\n\tSpearman: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " % \
                      (league, pearson, pp, bootstrapSamples, confidenceInterval, pLower, pUpper, spearman, sp, bootstrapSamples, confidenceInterval, sLower, sUpper)
            else:
                print "[Correlation Tester]:  Error! Arrays do not match for league %s. Length %d, %d" % (league, len(bets_array), len(pr_rel_entropy_array_reduced))

            attendance_array_reduced = attendance_array[4:15]
            if len(attendance_array_reduced) == len(value_array):
                [pearson,  pp] = correlationAnalyzr.calculateCorrelation(attendance_array_reduced, value_array, 'pearson')
                [spearman, sp] = correlationAnalyzr.calculateCorrelation(attendance_array_reduced, value_array, 'spearman')

                [pLower, pUpper] = correlationAnalyzr.bootstrapCorrelation(attendance_array_reduced, value_array, 'pearson', confidenceInterval, bootstrapSamples)
                [sLower, sUpper] = correlationAnalyzr.bootstrapCorrelation(attendance_array_reduced, value_array, 'spearman', confidenceInterval, bootstrapSamples)

                print "[Correlation Tester]:  Attendance and league value correlation for league %s:" \
                      "\n\tPearson: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " \
                      "\n\tSpearman: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " % \
                      (league, pearson, pp, bootstrapSamples, confidenceInterval, pLower, pUpper, spearman, sp, bootstrapSamples, confidenceInterval, sLower, sUpper)
            else:
                print "[Correlation Tester]:  Error! Arrays do not match for league %s. Length %d, %d" % (league, len(attendance_array_reduced), len(value_array))

            attendance_array_reduced = attendance_array[5:14]
            if len(attendance_array_reduced) == len(bets_array):
                [pearson, pp] = correlationAnalyzr.calculateCorrelation(attendance_array_reduced, bets_array, 'pearson')
                [spearman, sp] = correlationAnalyzr.calculateCorrelation(attendance_array_reduced, bets_array, 'spearman')

                [pLower, pUpper] = correlationAnalyzr.bootstrapCorrelation(attendance_array_reduced, bets_array, 'pearson', confidenceInterval, bootstrapSamples)
                [sLower, sUpper] = correlationAnalyzr.bootstrapCorrelation(attendance_array_reduced, bets_array, 'spearman', confidenceInterval, bootstrapSamples)

                print "[Correlation Tester]:  Attendance and bets volume correlation for league %s:" \
                      "\n\tPearson: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " \
                      "\n\tSpearman: %f, p: %f" \
                      "\n\t%d samples for confidence interval %d%%: [%f, %f] " % \
                      (league, pearson, pp, bootstrapSamples, confidenceInterval, pLower, pUpper, spearman, sp, bootstrapSamples, confidenceInterval, sLower, sUpper)
            else:
                print "[Correlation Tester]:  Error! Arrays do not match for league %s. Length %d, %d" % (league, len(attendance_array_reduced), len(bets_array))

            print ""
            print "-------------------------------------------------------------------------------------------------"

    print ""
    print ""
    print "-------------------------------------------------------------------------------------------------"

    if len(combined_attendance_array) == len(combined_pr_rel_entropy_array):
        [pearson, pp] = correlationAnalyzr.calculateCorrelation(combined_attendance_array, combined_pr_rel_entropy_array, 'pearson')
        [spearman, sp] = correlationAnalyzr.calculateCorrelation(combined_attendance_array, combined_pr_rel_entropy_array, 'spearman')

        [pLower, pUpper] = correlationAnalyzr.bootstrapCorrelation(combined_attendance_array, combined_pr_rel_entropy_array, 'pearson', confidenceInterval, bootstrapSamples)
        [sLower, sUpper] = correlationAnalyzr.bootstrapCorrelation(combined_attendance_array, combined_pr_rel_entropy_array, 'spearman', confidenceInterval, bootstrapSamples)

        print "[Correlation Tester]:  Attendance correlation for all leagues combined:" \
              "\n\tPearson: %f, p: %f" \
              "\n\t%d samples for confidence interval %d%%: [%f, %f] " \
              "\n\tSpearman: %f, p: %f" \
              "\n\t%d samples for confidence interval %d%%: [%f, %f] " % \
              (pearson, pp, bootstrapSamples, confidenceInterval, pLower, pUpper, spearman, sp, bootstrapSamples, confidenceInterval, sLower, sUpper)
    else:
        print "[Correlation Tester]:  Error! Arrays do not match for all leagues combined %s. Length %d, %d" % (len(attendance_array), len(pr_rel_entropy_array))


    # Visualizations
    folderName = 'output/graphs/correlation/'
    filename_attendance = 'attendance_correlation_over_leagues'
    filename_bets = 'bets_correlation_over_leagues'
    filename_league_value = 'league_value_correlation_over_leagues'

    visualizer.visualizeCorrelationAndIntervalsOverLeagues(folderName, filename_attendance, attendanceCorrelationsDictionary, 'Attendance Correlation Over Leagues', 'League', 'Attendance Correlation')
    visualizer.visualizeCorrelationAndIntervalsOverLeagues(folderName, filename_bets, betsCorrelationsDictionary, 'Bets Volume Correlation Over Leagues', 'League', 'Bets Volume Correlation')
    visualizer.visualizeCorrelationAndIntervalsOverLeagues(folderName, filename_league_value, leagueValueCorrelationsDictionary, 'Players Value (average of club per league) Correlation Over Leagues', 'League', 'Players Value (average of club per league) Correlation')


if __name__ == "__main__":
    main()
