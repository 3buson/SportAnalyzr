__author__ = '3buson'

import utils


def main():
    connection = utils.connectToDB()

    utils.calculateClubsSums(connection)


if __name__ == "__main__":
    main()
