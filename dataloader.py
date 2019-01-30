# Used to load price data in order to run simulation on historical price data
import csv
import time
import numpy as np
import pandas as pd

def timeit(f):

    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print('func:%r args:[%r, %r] took: %2.4f sec' %
          (f.__name__, args, kw, te-ts))
        return result

    return timed


def load_data_from_csv(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)

        data = [x for x in reader]
        return data


def load_data_pd_read_csv(file):
    names = ['time', 'price', 'unsure']
    return pd.read_csv(file, header=None, names=names)


def load_data_np_fromfile(file):
    with open(file, 'r') as f:
        print(np.fromfile(f, dtype=str, count=-1, sep=','))


if __name__ == '__main__':
    f = input('Price data file name: ')
    load = timeit(load_data_pd_read_csv)
    data = load(f)
    for row in data.itertuples():
        print(row)