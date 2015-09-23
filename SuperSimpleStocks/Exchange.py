__author__ = 'sachi'


'''The Exchange object holds stocks as a dictionary, encapsulating attributes by property decorators'''

from SuperSimpleStocks.Stock import Stock

#--------------------------------------------------------------------------------------------------------

class Exchange(object):

    def __init__(self, stocks={}):
        self.stocks = stocks
#--------------------------------------------------------------------------------------------------------

    #Property decorators to ensure encapsulation/hiding/etc. for class attributes


    @property
    def stocks(self):
        return self._stocks

    @stocks.setter
    def stocks(self, stocks):

        if type(stocks) is dict:
            self._stocks = stocks
        else:
            raise TypeError("Incorrectly Formatted StockList : Requiring StockDictionary object \
            (got "+ str(type(stocks))+")")


        self._stocks = stocks

#--------------------------------------------------------------------------------------------------------

    def addStock(self, stock):

        if type(stock) is Stock:
            self._stocks[stock.symbol] = stock
        else:
             raise TypeError("Incorrectly Formatted Stock : Requiring Stock object (got "+ str(type(stock))+")")

    def getStock(self, stock_symbol):

        if stock_symbol in self.stocks:
            return self.stocks[stock_symbol]
        else:
            raise ValueError("Invalid stock reference, no stocks found matching symbol "+ str(stock_symbol)+")")

#--------------------------------------------------------------------------------------------------------

    def GBCEAllShareIndex(self):

        #Calculates Geometric Mean (GBCE) of stocks in exchange

        stock_count = len(self.stocks)

        if stock_count is 0:
            return 0
        else:
            par_value_product = 1


            for x in self.stocks.values():
                par_value_product = x.par_value * par_value_product
            return pow(par_value_product, 1/stock_count)

#--------------------------------------------------------------------------------------------------------

    def __repr__(self):
        return "Stocks:\n"+"\n".join(str(x) for x in self.stocks.values())+"\n"

