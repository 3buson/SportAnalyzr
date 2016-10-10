__author__ = 'matic'

import utils


def main():
    connection = utils.connectToDB()

    utils.calculateClubsSums(connection)


if __name__ == "__main__":
    main()
