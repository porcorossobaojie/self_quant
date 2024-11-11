# -*- coding: utf-8 -*-
"""
Created on Fri Jul 16 16:17:42 2021

@author: Porco Rosso
"""

from __capital__.meta_obj.main import main, config, data_obj, link

import warnings
import numpy as np
from pandas import DataFrame as pdDataFrame
from pandas import Series as pdSeries
import pandas as pd
import __pandas

class DataFrame(pdDataFrame):
    
    _internal_names = pdDataFrame._internal_names + []
    _internal_names_set = set(_internal_names)
    _metadata = pdDataFrame._metadata

    @property
    def _constructor(self):
        return DataFrame

    @property
    def _constructor_sliced(self):
        return Series
    
    def data_init():
        data_obj.data_init()
    
    def chain(self, init_cash=10000):
        begin = pd.Timestamp.today()
        print(begin)
        df = self[self.index.isin(Series().__days__[1:])]
        init_beg = df.iloc[0].dropna()
        init_obj = Series(name=init_beg.day_shift(-1).name, cash=init_cash)
        lst = {init_beg.name: [link(init_obj, init_beg), round(init_cash, 2)]}
        count = 0
        for i, j in df.iterrows():
            try:
                position = list(lst.values())[-1][0].done.replace(0, np.nan).dropna()
                lst[i] = [link(position, j.dropna()), position.settle.total()]
                if position.name.month != j.name.month or i == df.index[-1]:
                    print(position.name, round(position.settle.total(),2))
            except:
                print('error %s' %(i))
                count += 1
            if count > 2:
                break
        print(pd.Timestamp.today() - begin)
        return lst
    
class Series(pdSeries, main):
    _internal_names = pdSeries._internal_names + []
    _internal_names_set = set(_internal_names)
    _metadata = pdSeries._metadata  + list(config.params.keys())

    @property
    def _constructor(self):
        return Series

    @property
    def _constructor_sliced(self):
        return Series
    
    def __init__(self, data=None, index=None, dtype=None, name=None, copy=False, fastpath=False, **kwargs):
        super(Series, self).__init__(data, index, dtype, name, copy, fastpath)
        params = config.params.copy()
        params.update({'_' + i: j for i,j in kwargs.items()})
        main.__init__(self, **params)

        
    @property
    def cash(self):
        return self._cash
    @cash.setter
    def cash(self, v):
        setattr(self, '_cash', v)
        
    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, v):
        setattr(self, '_state', v)
        
    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, v):
        setattr(self, '_unit', v)
        
    @property
    def settle(self):
        date = self.name
        columns = self.index
        key = self._settle_price
        
        def price():
            return self.__source__(date, key, columns)
        
        def assets(cash=None):
            if self.unit == 'cash' and cash is None:
                return self
            elif self.unit == 'cash' and cash is not None and self.cash == 0:
                return self / [self.sum(min_count=1)] * cash
            elif self.unit == 'cash' and cash is not None and self.cash != 0:
                raise ValueError('can not rebalance for cash is not 0')
            else:
                p = price()
                adj_assets = self[(self.notnull() & p.isnull())]
                x = self * p
                if len(adj_assets):
                    shift = -1
                    while True:
                        try:
                            x.cash = x.cash + adj_assets.day_shift(shift).settle.assets().sum()
                            break
                        except:
                            shift -= 1
                x.unit = 'cash'
                return x
            
        def share():
            if self.unit == 'share':
                    return self
            else:
                p = price()
                adj_assets = self[(self.notnull() & p.isnull())]
                x = self / p
                if len(adj_assets):
                    shift = -1
                    while True:
                        try:
                            x.cash = x.cash + adj_assets.day_shift(shift).settle.assets().sum()
                            break
                        except:
                            shift -= 1
                x.unit = 'share'
                return x
            
        def total():
            return assets().sum() + self.cash
            
        obj = type('settle', (), {'price':price, 'assets': assets, 'share': share, 'total':total})
        return obj
    
    @property
    def trade(self):
        date = self.name
        columns = self.index
        key = self._trade_price
        
        def price():
            return self.__source__(date, key, columns)
        
        def assets(cash=None):
            if self.unit == 'cash' and cash is None:
                return self
            elif self.unit == 'cash' and cash is not None and self.cash == 0:
                return self / [self.sum(min_count=1)] * cash
            elif self.unit == 'cash' and cash is not None and self.cash != 0:
                raise ValueError('can not rebalance for cash is not 0')
            else:
                x = self * price()
                x.unit = 'cash'
                return x
            
        def share():
            if self.unit == 'share':
                return self
            else:
                x = self / price()
                x.unit = 'share'
                return x
            
        def cost():
            x = assets().abs() * self._trade_cost * -1
            return x
        
        def limit(trade_status=True, buy_limit=True, sell_limit=True, detail=False):
            date = self.name
            columns = self.index
            x = self.__source__(date, [self._pct_change_key, self._buy_limit_key, self._sell_limit_key, self._trade_status_key], columns).unstack(0)
            if len(x):
                x['Buyable'] = x[self._buy_limit_key] >= self._buy_limit
                x['Sellable'] =  x[self._sell_limit_key] >= self._sell_limit
                x['Tradeable'] = True
                x['Order'] = self
                if trade_status:
                    x['Tradeable'] = x[self._trade_status_key].fillna(False)
                if buy_limit:
                    x['Tradeable'][(self > 0) & (~x['Buyable'])] = False
                if sell_limit:
                    x['Tradeable'][(self <= 0) & (~x['Sellable'])] = False
            else:
                x = pd.DataFrame(columns=[self._pct_change_key, self._trade_status_key, 'Buyable', 'Sellable', 'Tradeable', 'Order'])
            if detail:
                x = x[[self._pct_change_key, self._trade_status_key, 'Buyable', 'Sellable', 'Tradeable', 'Order']].loc[:, [True, trade_status, buy_limit, sell_limit, True, True]]
                x = DataFrame(x)
                x.columns.name = date
            else:
                x = x['Order'][x['Tradeable']].rename(date)
                x = Series(x, unit=self.unit)
            return x
                
        def total(cost=True):
            x = assets().sum() + self.cash
            x = x + cost() if cost else x
            return x
            
        def rebalance():
            x = self.copy()
            x.cash = assets().sum() * -1
            return x
            
        obj = type('trade', (), {'price':price, 'assets': assets, 'share': share, 'cost': cost, 'limit': limit, 'total': total, 'rebalance': rebalance})
        return obj
    
    def source(self, keys):
        return self.__source__(self.name, keys, self.index)
            
    def __calcable__(self, obj):
        return getattr(obj, 'unit', self.unit) == self.unit
        
    def __state__(self, obj):
        x = [getattr(i, 'state', self.state) for i in [self, obj]]
        x = set(x)
        x = config.params['_state'] if len(x) > 1 else x.pop()
        return x
        
    
    def __add__(self, obj):
        if self.__calcable__(obj):
            x = super().__add__(obj)
            x.state = self.__state__(obj)
            x.cash = x.cash + getattr(obj, 'cash', 0)
            x.name = max([self.name, getattr(obj, 'name', self.name)]) 
            return x
        else:
            raise ValueError()
            
    def add(self, other, fill_value=0):
        x = super().add(other, fill_value=fill_value)
        x.state = self.__state__(other)
        x.cash = x.cash + getattr(other, 'cash', 0)
        x.name = max([self.name, getattr(other, 'name', self.name)]) 
        return x
    
    def __sub__(self, obj):
        if self.__calcable__(obj):
            x = super().__sub__(obj)
            x.state = self.__state__(obj)
            x.cash = x.cash - getattr(obj, 'cash', 0)
            x.name = max([self.name, getattr(obj, 'name', self.name)]) 
            return x
        else:
            raise ValueError()
            
    def sub(self, other, fill_value=0):
        x = super().sub(other, fill_value=fill_value)
        x.state = self.__state__(other)
        x.cash = x.cash + getattr(other, 'cash', 0)
        x.name = max([self.name, getattr(other, 'name', self.name)]) 
        return x
                            
    def __mul__(self, obj):
        if isinstance(obj, (int, float, np.number)):
            x = super(Series, self).__mul__(obj)
            x.cash = x.cash * obj
        else:
            x = super().__mul__(obj)
        x.name = self.name
        x.state = self.state
        return x
    
    def __truediv__(self, obj):
        if isinstance(obj, (int, float, np.number)):
            x = super(Series, self).__truediv__(obj)
            x.cash = x.cash / obj
        else:
            x = super().__truediv__(obj)
        x.state = self.state
        x.name = self.name
        return x
    
    def day_shift(self, shift=1, name=None):
        x = self.copy()
        if name is not None:
            x.name = pd.to_datetime(name)
        else:
            x.name = self.__shift__(self.name, shift)
        return x
