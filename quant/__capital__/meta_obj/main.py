# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 16:14:27 2021

@author: Porco Rosso
"""

import numpy as np
import pandas as pd
from __capital__.data_obj.main import main as data_obj
from __capital__.meta_obj.config import main as config
data_obj = data_obj()

class main():
    def __init__(self, **kwargs):
        params = config.params.copy()
        params.update(kwargs)
        [setattr(self, i, j) for i,j in params.items()]
        
    @property
    def __data__(self):
        return data_obj
        
    def __source__(self, date, key, columns):
        return self.__data__.__source__(date, key, columns)
    
    @property
    def __price_key__(self):
        str_obj = self.state
        return getattr(self, str_obj + '_price')
    
    @property
    def __days__(self):
        return self.__data__.__days__
    
    def __price__(self, date, columns):
        return self.__source__(date, self.__price_key__, columns)
    
    def __trade_status__(self, date, columns, reverse=False):
        return self.__data__.__trade_status__(date, columns)
    
    def __is_ST__(self, date, columns):
        return self.__data__.__is_ST__(date, columns)
    
    def __buy_limit__(self, date, columns, reverse=True):
        return self.__data__.__buy_limit__(date, columns, self._buy_limit, reverse)
    
    def __sell_limit__(self, date, columns, reverse=True):
        return self.__data__.__sell_limit__(date, columns, self._sell_limit, reverse)
    
    def __shift__(self, date, shift):
        return self.__data__.__shift__(self.__days__, date, shift)
    
    
class link():
    def __init__(self, position, beg):
        self._reset = True
        self.position = position
        self.beg = beg
                
    @property
    def position(self):
        return self._position.share
    @position.setter
    def position(self, v):
        v = v.settle.assets().replace(0, np.nan).dropna()
        obj = {'assets': v.settle.assets(), 'share': v.settle.share()}
        self._position = type('position', (), obj)
        
    @property
    def beg(self):
        return self._beg.share
    @beg.setter
    def beg(self, v):
        v = v.day_shift(-1)
        position = self._position.share.rename(v.name)
        assets = v.settle.assets(position.settle.total())
        share = assets.settle.share()
        obj = {'assets': assets.day_shift(1), 'share': share.day_shift(1)}
        self._beg = type('beg', (), obj)
        
    @property
    def order(self):
        x = self._beg.share.sub(self._position.share)
        x.cash = 0
        return x
    
    @property
    def cost(self):
        return self.limit(False).trade.cost()
    
    @property
    def untrade(self):
        return self.order.sub(self.limit(False), fill_value=0).replace(0, np.nan).dropna()
    
    @property
    def turnover(self):
        return self.action(False).abs().settle.assets().sum() / self._position.assets.settle.total()
    
    def limit(self, detail=True):
        return self.order.trade.limit(detail=detail)

    def action(self, cost=True):
        x = self.order.trade.limit().dropna()
        x.cash = -x.trade.assets().sum()
        if cost:
            x.cash = x.cash + x.trade.cost().sum()
        return x
    
    @property
    def done(self):
        x = self._position.share.add(self.action(True))
        return x
    
    @property
    def different(self):
        position = self._position.share.rename('Position')
        beg = self._beg.share.rename('Beg')
        order = self.order
        order_price = order.day_shift(-1).settle.price().rename('Order_Price')
        action = self.action(cost=False)
        action_price = action.trade.price().fillna(order_price).rename('Trade_Price')
        trade_diff = (order * order_price - action * action_price).rename('Trade_Diff')
        trade_cost = self.cost.rename('Trade_Cost')        
        order = order.rename('Order')
        action = action.rename('Trade')
        untrade = self.untrade
        untrade_price = untrade.trade.price().fillna(untrade.day_shift(-1).settle.price())
        untrade_diff = untrade * untrade.day_shift(-1).settle.price() - untrade * untrade_price
        untrade = untrade.rename('Untrade')
        untrade_price = untrade_price.rename('Untrede_price')
        untrade_diff = untrade_diff.rename('Untrade_Diff')
        df = pd.concat([position, beg, order, order_price, action, action_price, trade_diff, trade_cost, untrade, untrade_price, untrade_diff], axis=1)
        df = df[~df[['Position', 'Beg', 'Order']].isnull().all(axis=1)]
        
        weight = self.position
        lst = [(self.beg.settle.total() / weight.settle.total() - 1) if len(self.beg.settle.assets()) else 0, 
               df['Trade_Diff'].sum() / weight.settle.total(), 
               df['Trade_Cost'].sum() / weight.settle.total(), 
               df['Untrade_Diff'].sum() / weight.settle.total(), 
               self.done.settle.total() / weight.settle.total() - 1]
        lst = pd.Series(lst, name=weight.day_shift(1).name, index=['Theoretical_Return', 'Trade_Different', 'Trade_Cost', 'Untrade_Different', 'Effective_Return'])
        obj = type('different', (), {'detail': df, 'returns':lst})
        return obj
        
        
    
    
    


















