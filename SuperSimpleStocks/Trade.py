__author__ = 'sachi'

from datetime import datetime
from enum import Enum, unique

'''The trade class below holds the necessary attributes to specify trades for a stock/shares. It overloads three
comparison operators so that trade objects can be ordered by timestamp, which is necessary to enable
storage in an ordered list (see Stock module). Property decorators are used to encapsulate attributes, and an enumerated
type (TradeType) to hold an unique trade-type
'''

#--------------------------------------------------------------------------------------------------------

@unique
class TradeType(Enum):
    BUY = 1
    SELL = 2

#--------------------------------------------------------------------------------------------------------

class Trade(object):

    def __init__(self, timestamp, share_quantity, trade_type, trade_price):
        self.timestamp = timestamp
        self.share_quantity = share_quantity
        self.trade_type = trade_type
        self.trade_price = trade_price

#--------------------------------------------------------------------------------------------------------

    #The following allows trade objects to be compared to other trade objects or timestamps
    def __lt__(self, other):
        if type(other) is Trade:
            return self._timestamp <  other.timestamp
        elif type(other) is datetime:
            return self._timestamp < other

    def __gt__(self, other):
        if type(other) is Trade:
            return self._timestamp >  other.timestamp
        elif type(other) is datetime:
            return self._timestamp > other


    def __eq__(self, other):

        if type(other) is Trade:
            return self._timestamp is  other.timestamp
        elif type(other) is datetime:
            return self._timestamp is other

#--------------------------------------------------------------------------------------------------------

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        if type(timestamp) is datetime:
            self._timestamp = timestamp
        else:
            raise TypeError("Incorrectly Formatted Timestamp : Requiring datetime object (got "+ str(type(timestamp))+")")

#--------------------------------------------------------------------------------------------------------

    @property
    def share_quantity(self):
        return self._share_quantity

    @share_quantity.setter
    def share_quantity(self, share_quantity):

        if type(share_quantity) is not int:
            raise TypeError("Invalid type for share quantity : Requiring positive integer (got "+ str(type(share_quantity))+")")

        elif share_quantity <= 0:
            raise TypeError("Invalid value for share quantity : Requiring positive integer (got "+ str(share_quantity)+")")
        else:
            self._share_quantity = share_quantity

#--------------------------------------------------------------------------------------------------------

    @property
    def trade_type(self):
        return self._trade_type

    @trade_type.setter
    def trade_type(self, trade_type):

        if type(trade_type) is not TradeType:
            raise TypeError("Invalid trade type : Requiring StockType object (got "+ str(type(trade_type))+")")

        elif (trade_type != TradeType.BUY and trade_type != TradeType.SELL):
            raise ValueError("Invalid trade type: Requiring BUY or SELL (got "+ str(trade_type)+")")

        else:
            self._trade_type = trade_type

#--------------------------------------------------------------------------------------------------------

    @property
    def trade_price(self):
        return self._trade_price

    @trade_price.setter
    def trade_price(self, trade_price):
        self._trade_price = trade_price

#--------------------------------------------------------------------------------------------------------

    def __repr__(self):
        return "< Time (UTC) : "+str(self._timestamp) + " | QT : " + str(self._share_quantity) + \
               " | Type : "+str(self._trade_type.name) + "  | Price : " + str(self._trade_price)+" >"


