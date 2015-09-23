__author__ = 'sachi'


'''This class does some very basic testing of the modules in SuperSimpleStocks. Apart from some
basic unit tests that ensure that invalid data is being dealt with (by exceptions), it efficiently creates a random
exchange wih trades, that checks for normal-function'''

import numpy.random as npr
import random, string, unittest
import time, gc
from datetime import datetime, timedelta
from SuperSimpleStocks.Stock import Stock, StockType
from SuperSimpleStocks.Exchange import Exchange
from SuperSimpleStocks.Trade import TradeType

import timeit

#--Class for Unit testing Stocks-------------------------------------------------------------------------
class TestStocks(unittest.TestCase):

#Check invalid stock data types is being handled
  def test_type_checks(self):
      with self.assertRaises(TypeError):
          Stock(2,StockType.Common,12,12)
          Stock("ASX",4,12,12)
          Stock("ASX",StockType.Common,'s',12)
          Stock("ASX",StockType.Common,12,'s')
          Stock("ASX",StockType.Preferred,12,12,'s')
          Stock("ASX",StockType.Preferred,12,12)


#Check invalid stock data is being handled, check boundaries

  def test_validity_checks(self):
      with self.assertRaises(ValueError):
          Stock("ASXA",StockType.Common,12,12)
          Stock("ASX",StockType.Common,-1,12)
          Stock("ASX",StockType.Common,12,-1)
          Stock("ASX",StockType.Preferred,12,-1)
          Stock("ASX",StockType.Preferred,12,101)


#==Run above Unit tests for Stocks=====
suite = unittest.TestLoader().loadTestsFromTestCase(TestStocks)
unittest.TextTestRunner(verbosity=2).run(suite)
#--------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
#Efficiently Generate Random Stock/Trade Data using NumPy's Random Sampler
#--Pre-generate random numbers to later be used for test data----------------------------
RANDOM_PRESET_SIZE = 10000
#----------------------------------------------------------------------------------------
rand_last_div = npr.randint(0,100, size=RANDOM_PRESET_SIZE).tolist()
rand_fixed_div = npr.randint(1,100, size=RANDOM_PRESET_SIZE).tolist()
rand_par_value = npr.randint(1,1000, size=RANDOM_PRESET_SIZE).tolist()
rand_share_quantity = npr.randint(1,100, size=RANDOM_PRESET_SIZE)
rand_price = npr.randint(1,1000, size=RANDOM_PRESET_SIZE)
rand_timestamp = [datetime.utcnow()-timedelta(minutes=x) \
                  for x in range (RANDOM_PRESET_SIZE)]
#--------------------------------------------------------------------------------------------------------

rand_stock_symbols = [(''.join(random.choice(string.ascii_uppercase) \
                               for _ in range(3))) for r in range(RANDOM_PRESET_SIZE)]
rand_stock_types = [random.choice(list(StockType)) for r in range(RANDOM_PRESET_SIZE)]
rand_trade_types = [random.choice(list(TradeType)) for r in range(RANDOM_PRESET_SIZE)]
#--------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------
#Functions for generating random stocks given an exchange, and random trades given stock

def addRandomStocks(ex, count):

    for x in range(count):
        if (rand_stock_types[x] is StockType.Preferred):
            ex.addStock(Stock(rand_stock_symbols[x],rand_stock_types[x], rand_last_div[x],\
                              rand_par_value[x], rand_fixed_div[x]))
        else:
            ex.addStock(Stock(rand_stock_symbols[x],rand_stock_types[x], rand_last_div[x],rand_par_value[x]))

def addRandomTrades(stock, count):

    for x in range(count):
        stock.addTrade(rand_timestamp[x], int(rand_share_quantity[x]), rand_trade_types[x], int(rand_price[x]))

#--------------------------------------------------------------------------------------------------------
def makeRandomExchange(exchange, stock_count, trade_count):

    addRandomStocks(exchange, stock_count)

    for key in exchange.stocks:
        addRandomTrades(exchange.getStock(key),trade_count)
#--------------------------------------------------------------------------------------------------------
'''def effProfile(stock_count, trade_count):


    print ("Efficiency Tests")
    if(stock_count>RANDOM_PRESET_SIZE or trade_count>RANDOM_PRESET_SIZE):
        print ("Test set size too large, max=", RANDOM_PRESET_SIZE)
    else:
        testEx = Exchange()
        start_time = time.time()
        makeRandomExchange(testEx, stock_count,trade_count)
        print("Created %s stocks with %s trades each in  %0.4f seconds ---" % (stock_count,trade_count, (time.time() - start_time)))
'''
def main():

#------Create efficiency-profile with randomly generated data

    #effProfile(100, RANDOM_PRESET_SIZE)
    #gc.collect()

#------Do normal tests with randomly generated Data (validity tests done above)
    print("Normal Test")

    ex = Exchange()
    makeRandomExchange(ex,5,5)

    print (ex)

    #Do Calculations based on random stock
    market_price = random.randint(1,100)
    random_stock_key = list(ex.stocks.keys())[random.randint(0,len(ex.stocks.keys())-1)]

    print ("Dividend Yield, %0.4f"% ex.getStock(random_stock_key).dividend_yield(market_price))
    print ("PERation, %0.4f"% (ex.getStock(random_stock_key).PERatio(market_price)))
    print ("VWSP, %0.4f" % (ex.getStock(random_stock_key).getVolumeWeightedStockPrice()))
    print ("GBCE, %0.4f" % (ex.GBCEAllShareIndex()))



main()
