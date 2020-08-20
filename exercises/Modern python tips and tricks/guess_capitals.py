import csv
import random
import sys


def get_capitals(file_name):
    """Open capitals CSV file and return list of capital tuples."""
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip headers row
        return [(place, capital) for place, capital in csv_reader]


def main(file_name):
    capitals = get_capitals(file_name)
    place, capital = random.choice(capitals)
    while True:
        guess = input("What is the capital of {}? ".format(place))
        if guess == capital:
            print("Correct! {} is the capital of {}".format(capital, place))
            break
        else:
            print("That's not correct.  Try again.")


if __name__ == "__main__":
    main(sys.argv[1])
