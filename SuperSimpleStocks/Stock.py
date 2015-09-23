__author__ = 'sachi'


'''The stock class below holds the necessary attributs to specify stocks on the exchange ,
it also holds information about trades, keeping them inside a sorted-(tree based)-list for efficient lookup.
This is is important especially since a high volume of trades are expected, and the microseconds of lag in looking up
trade data (that an increase/decrease of algorithmic complexity would entail) could lead to inconsistent/inaccurate
calculations involving that data'''

import bisect

from datetime import timedelta
from SuperSimpleStocks.Trade import *

#--------------------------------------------------------------------------------------------------------

#Unique decorator ensures only one name is bound to any one value.

@unique
class StockType(Enum):
    Preferred = 1
    Common = 2

#--------------------------------------------------------------------------------------------------------

class Stock(object):

    '''All values here will be set through the properites below, to enable type and validity checks'''

    def __init__(self, symbol, stock_type, last_dividend, par_value, fixed_dividend=None):
        self.symbol = symbol
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value
        self.trades = []
#--------------------------------------------------------------------------------------------------------

#Getter and setter functions for each property sets `_property', which works to hide it and encapsulate it,
#this is roughly equivalent to Java's 'protected'

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):

        if type(symbol) is not str:
            raise TypeError("Invalid type for stock symbol : Requiring 3-letter string (got "+ str(type(symbol))+")")
        elif (len(symbol) != 3) :
            raise ValueError("Invalid stock symbol: Requiring 3-letter string (got "+ str(symbol)+")")
        else:
            self._symbol = symbol.upper()
#--------------------------------------------------------------------------------------------------------

    @property
    def stock_type(self):
        return self._stock_type

    @stock_type.setter
    def stock_type(self, stock_type):

        if type(stock_type) is not StockType:
            raise TypeError("Invalid stock type : Requiring StockType object (got "+ str(type(stock_type))+")")
        elif (stock_type != StockType.Preferred and stock_type != StockType.Common):
            raise ValueError("Invalid stock type: Requiring Preferred or Common (got "+ str(stock_type)+")")
        else:
            self._stock_type = stock_type

#--------------------------------------------------------------------------------------------------------

    @property
    def last_dividend(self):
        return self._last_dividend

    @last_dividend.setter
    def last_dividend(self, last_dividend):

        if type(last_dividend) is not int:
            raise TypeError("Invalid type for Last Dividend : Requiring positive integer (got "+ str(type(last_dividend))+")")
        elif (last_dividend <0):
            raise ValueError("Invalid value for last dividend: Requiring positive integer (got "+ str(last_dividend)+")")
        else:
            self._last_dividend = last_dividend

#--------------------------------------------------------------------------------------------------------

    @property
    def fixed_dividend(self):
        return self._fixed_dividend

    @fixed_dividend.setter
    def fixed_dividend(self, fixed_dividend):

        div_type = type(fixed_dividend)

        #The following checks for consistency between stock type and specification of a fixed dividend

        if (div_type not in [type(None), float, int]):
            raise TypeError("Invalid type for Last Dividend : Requiring float or absent value (got "+ str(type(fixed_dividend))+")")

        elif (div_type is type(None)) and (self.stock_type is StockType.Preferred):
            print("here")
            raise TypeError("Invalid Stock type for unspecified fixed dividend, expected type 'Common' (got "+ str(self.stock_type)+")")

        elif (div_type is not type(None)) and ((fixed_dividend < 0) or (fixed_dividend >100)):
            raise ValueError("Invalid value for last dividend: Requiring number between 1 and 100 (got "+ str(fixed_dividend)+")")
        else:
            self._fixed_dividend = fixed_dividend

#--------------------------------------------------------------------------------------------------------


    @property
    def par_value(self):
        return self._par_value

    @par_value.setter
    def par_value(self, par_value):

        if type(par_value) is not int:
            raise TypeError("Invalid type for par value : Requiring positive integer, (got "+ str(type(par_value))+")")
        elif par_value < 0:
            raise ValueError("Invalid par-value : Requiring positive integer, (got "+ str(par_value)+")")

        else:
            self._par_value = par_value

#--------------------------------------------------------------------------------------------------------


    def dividend_yield(self, market_price):


        #The following catches a divide-by-zero error

        if market_price <=0:
            raise ValueError("Invalid market-price : Requiring non-zero float, (got "+ str(market_price)+")")

        elif self.stock_type is StockType.Common:
             return self.last_dividend/market_price
        else:
            return (self.fixed_dividend*self.par_value)/market_price

    def PERatio(self, market_price):

        #The following catches the two cases where the PERatio cannot be calculated

        if self.stock_type is StockType.Common:
            if (self.last_dividend is 0):
                raise ValueError("PERatio Not available, last dividend was 0")
            else:
                return market_price/self.last_dividend

        elif (self.fixed_dividend is None or self.par_value is 0):
             raise ValueError("PERatio Not available, fixed dividend or par-value was 0")
        else:
            return market_price/(self.fixed_dividend*self.par_value)

#--------------------------------------------------------------------------------------------------------


    def getVolumeWeightedStockPrice(self):


        #Calculate the timestamp for fifteen minutes ago
        periodPast = datetime.utcnow()-timedelta(minutes=15)

        #Find place in list where 15minutes ago would fit.
        #If item is already present in list, the insertion point will be before (to the left of) any existing entries

        period_start_point = bisect.bisect(self.trades, periodPast)

        #Get a slice of the trades list that corresponds to this last 15 minutes
        period_trades = self.trades[period_start_point:]

        #Calculate the quantities and volume weighted stock price for non-zero trades
        quantities = sum(x.share_quantity for x in period_trades)
        volume = sum(x.trade_price * x.share_quantity for x in period_trades)

        if quantities>0:
            return volume/quantities
        else:
            raise ValueError("Unable to calculate Volume Weighted Stock Price, non-zero quantity required")

#--------------------------------------------------------------------------------------------------------


    def addTrade(self, timestamp, share_quantity, trade_type, trade_price):

        '''Keep the trade-list sorted by timestamp, inserting new trade into appropriate position
        using a bisection algorithm (O(log n) for insert and find)'''

        bisect.insort(self.trades, Trade(timestamp, share_quantity, trade_type, trade_price))

#--------------------------------------------------------------------------------------------------------

    def __repr__(self):

        #String representation for class, used when str()/print function is called on class
        # The last bit form a string of trade descriptions using list comprehension

        return "< "+self.symbol + " | Type : "+ str(self.stock_type.name) +" | LastDiv: "+ str(self.last_dividend) + \
               " | FixedDividend: " + str(self.fixed_dividend)+ " | Par_Value: "+ str(self.par_value)+ " >" + \
               "\n\n\t\t"+"Trades".center(70,"=")+"\n\n\t"+"\n\t".join(str(x) for x in self.trades)+"\n"
