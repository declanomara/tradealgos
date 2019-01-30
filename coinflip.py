# Algorithm:
# Flip a coin, pick either up or down
# Set stop loss and buy stop
# Repeat

# TODO
# Implement algorithm
# Implementing trailing stop loss and buy stop
# Optimize

import random
import sys
import multiprocessing
from dataloader import load_data_pd_read_csv

'''
BALANCE_USD = 10000
BALANCE_BTC = 0
TRADES = 0
MAX_LOSS = 0
MAX_GAIN = 0
BIG = .2
SMALL = .1
TRAIL = .95


class Position:
    def __init__(self, upper, lower, trail, type):
        # Upper: threshold to meet before considering selling
        # Lower: threshold to meet to sell
        # Trail: fraction of peak to sell at
        self.type = type
        self.upper = upper
        self.lower = lower
        self.trail = trail
        self.peak = 0

    def check_sell(self, price):
        if price > self.peak:
            self.peak = price
            return False

        elif price < self.peak:
            if self.peak < self.upper:
                return False
            else:
                return price <= (self.peak * self.trail)

        elif price < self.lower:
            return True

    def check_buy(self, price):
        if price > self.upper:
            return True

        elif price < self.peak:
            self.peak = price
            return False

        elif self.peak < price:
            if self.peak > self.lower:
                return False

            else:
                return price >= (self.peak * self.trail)



def trade(row, position):
    global BALANCE_USD
    global BALANCE_BTC
    # Row [time, price, idk]
    # Position class Position(upper, lower)

    price = row[1]

    # If we don't have a position flip a coin
    if position is None:
        prediction = bool(randint(0,1))
        if prediction:
            # Price going up
            upper = price + (price * BIG)
            lower = price - (price * SMALL)

            BALANCE_BTC = BALANCE_USD/price
            BALANCE_USD = 0

            return Position(upper, lower, TRAIL, prediction)

        else:
            # Price going down
            upper = price + (price * SMALL)
            lower = price - (price * BIG)

            return Position(upper, lower, TRAIL, prediction)

    else:
        if position.type:
            if position.check_sell(price):
                print(f'SOLD BTC {price}')
                BALANCE_USD = BALANCE_BTC * price
                BALANCE_BTC = 0
                return None

        else:
            if position.check_buy(price):
                print(f'BOUGHT BTC {price}')
                return None
'''

class Trader:
    def __init__(self, data, BIG, SMALL, TRAIL):
        self.data = data
        self.bal_USD = 10000
        self.bal_BTC = 0
        self.BIG = BIG
        self.SMALL = SMALL
        self.TRAIL = TRAIL
        self.upperlim = None
        self.lowerlim = None
        self.extreme = None
        self.prediction = None

    def initialize(self, row):
        self.buy(row)

    def buy(self, row):
        price = row[2]
        self.bal_BTC = self.bal_USD / price
        self.bal_USD = 0
        # print(f'{row[0]} BOUGHT AT {price} BTC: {self.bal_BTC} USD: {self.bal_USD}')

        self.upperlim = price + price * self.BIG
        self.lowerlim = price - price * self.SMALL
        # print(f'{row[0]} NEXT SELL AT {self.lowerlim}')

        self.extreme = -1
        self.prediction = 'UP'

    def sell(self, row):
        price = row[2]
        self.bal_USD = self.bal_BTC * price
        self.bal_BTC = 0
        # print(f'{row[0]} SOLD AT {price} BTC: {self.bal_BTC} USD: {self.bal_USD}')

        self.upperlim = price + price * self.SMALL
        self.lowerlim = price - price * self.BIG
        # print(f'{row[0]} NEXT BUY AT {self.upperlim}')

        self.extreme = 30000 # TODO Properly implement a big number
        self.prediction = 'DOWN'

    def trade(self, row):
        price = row[2]
        if self.prediction == 'UP':
            if price < self.lowerlim:
                self.sell(row)

            elif price > self.extreme:
                self.extreme = price

            elif price < self.extreme:
                if self.extreme > self.upperlim:
                    if price <= self.extreme * self.TRAIL:
                        self.sell(row)

        elif self.prediction == 'DOWN':
            if price > self.upperlim:
                self.buy(row)

            elif price < self.extreme:
                self.extreme = price

            elif price > self.extreme:
                if self.extreme < self.lowerlim:
                    if price >= self.extreme * self.TRAIL:
                        self.buy(row)

        else:
            raise Exception('Failed to initialize')

    def calc_return(self):
        if self.bal_USD > 0:
            return self.bal_USD/10000
        else:
            return self.bal_BTC/33.3333


    def simulate(self):
        row = next(self.data)
        self.initialize(row)

        for row in self.data:

            self.trade(row)
            if self.calc_return() < .8:
                return self.calc_return()

        return self.calc_return()


def simulation_proc(data, result_q):
    BIG = random.uniform(.02, .20)
    SMALL = BIG * random.uniform(0, 1)
    TRAIL = random.uniform(.8, 1)
    trader = Trader(data, BIG, SMALL, TRAIL)
    returns = trader.simulate()
    results = (BIG, SMALL, TRAIL, returns)
    result_q.put(results)


def results_proc(result_q):
    best = 0
    while True:
        BIG, SMALL, TRAIL, returns = result_q.get()
        if returns > best:
            best = returns
            print(f'BIG: {BIG} SMALL: {SMALL} TRAIL: {TRAIL} RETURN: {returns}')


if __name__ == '__main__':
    file = sys.argv[1]
    data = load_data_pd_read_csv(file).itertuples()

    result_q = multiprocessing.Queue()

    processes = []
    for i in range(100):
        p = multiprocessing.Process(target=simulation_proc, args=(data, result_q))
        p.start()
        p.daemon = True
        processes.append(p)

    results_proc(result_q)
