__author__ = '3buson'

from CSVParser import csvParser


def main():
    # csvParser.parseBetsCSVFile('FileConqueror/csv/bets/raw/', ',')
    csvParser.parseBetsCSVFileByGame('FileConqueror/csv/bets/raw/', ',')


if __name__ == "__main__":
    main()
