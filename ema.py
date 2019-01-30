# Algorithm
# Slow and fast moving exponential average, when fast crosses slow, indicates buy or sell depending on direction

import random
import sys
import multiprocessing
from dataloader import load_data_pd_read_csv


class Trader:
    def __init__(self, data):
        self.data = data

    def buy(self):
        pass

    def sell(self):
        pass


def buy(usd, price):
    btc = usd/price
    return (0, btc)


def sell(btc, price):
    usd = btc * price
    return (usd, 0)


def value(btc, usd, price):
    if btc == 0:
        return usd

    else:
        return usd + (btc*price)


if __name__ == '__main__':
    file = sys.argv[1]
    data = load_data_pd_read_csv(file)
    data = data.itertuples()

    initial_price = next(data)[2]
    slow_ma = initial_price
    fast_ma = initial_price

    fast = .2
    slow = .02

    direction = ''

    usd = 10000
    btc = 0

    prev_value = value(btc, usd, initial_price)
    maxgain = 0
    maxloss = 0

    print('initialized')
    for row in data:
        else:
            print(row[0])
            #quit()
        if usd < 0:
            quit()

        if btc < 0:
            quit()
        price = row[2]
        fast_ma = price * fast + fast_ma * (1-fast)
        slow_ma = price * slow + slow_ma * (1-slow)

        if fast_ma > slow_ma:
            if direction != 'rising':
                usd, btc = buy(usd, price)
            direction = 'rising'
        else:
            if direction != 'falling':
                usd, btc = sell(btc, price)
            direction = 'falling'

        if value(btc, usd, price) != prev_value:
            delta = value(btc, usd, price) - prev_value
            if delta < maxloss:
                maxloss = delta
            if delta > maxgain:
                maxgain = delta

        print(f'fast_ma: {fast_ma} slow_ma: {slow_ma} price: {price} USD: {usd} BTC: {btc} Loss: {maxloss} Gain: {maxgain}')

