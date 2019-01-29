# Used to load price data in order to run simulation on historical price data
import csv


def load_data_from_csv(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)

        for row in reader:
            print(row)


if __name__ == '__main__':
    load_data_from_csv('krakenUSD.csv')