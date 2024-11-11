 # -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 12:41:33 2022

@author: Porco Rosso
"""

from __trade__.__data_source__.main import main as data_source
from __trade__.main.config import main as config

from pandas import DataFrame as pdDataFrame
from pandas import Series as pdSeries
import pandas as pd
import numpy as np
import __pandas


class data_params(type('data', (), config.static_info)):    
    data_source = data_source(**{i[1:]:j for i,j in config.static_info.items()})

    
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
    '''
    def chain(self, init_cash=10000, standard=False, show=True):
        begin = pd.Timestamp.today()
        print(begin)
        days = list(Series.data_source.internal_data.values())[0].index
        df_obj = self.loc[days[0]: days[-1]]
        dic = {}
        hold = link(df_obj.iloc[0].dropna().settle.assets(init_cash).settle.share(), None, init_cash, standard)
        dic[hold.hold.name] = hold
        count = 0
        for i, j in df_obj.iloc[1:-1].iterrows():
            try:
                hold = hold(j.dropna(), standard=standard)
                dic[hold.hold.name] = hold
                if days[days.get_loc(i) + 1].month != j.name.month or i == df_obj.index[-2]:
                    if show:
                        print(i, round(hold.hold.settle.tot_assets(), 2))
            except:
                print('error %s' %(i))
                count += 1
            if count > 2:
                break
        def returns():
            x = {i:j.hold.settle.tot_assets() for i,j in dic.items()}
            last = list(dic.values())[-1].done
            x[last.name] = last.settle.tot_assets()
            x = pd.Series(x)
            return x
        
        print(pd.Timestamp.today() - begin)
        return dic
        '''
    def chain(self, init_cash=10000, standard=False, show=True):
        x = chain(self, init_cash, standard, show)
        x()
        return x

class Series(pdSeries, data_params):
    _internal_names = pdSeries._internal_names + []
    _internal_names_set = set(_internal_names)
    _metadata = pdSeries._metadata  + list(config.instance_info.keys())

    @property
    def _constructor(self):
        return Series

    @property
    def _constructor_sliced(self):
        return Series
    
    def __init__(self, data=None, index=None, dtype=None, name=None, copy=False, fastpath=False, **kwargs):
        params = config.instance_info.copy()
        params.update({'_' + i: j for i,j in kwargs.items()})
        [setattr(self, i, j) for i,j in params.items()]
        super(Series, self).__init__(data, index, dtype, name, copy, fastpath)
    
    def __select__(self, key):
        name = self.index if self.name is None else self.name
        return self.data_source.__select__(key, name, self.index)
    
    def __repr__(self):
        x = super().__repr__()
        x = x + '\nstate: %s, unit: %s, \ncount: %s, cash: %s, \nis_adj: %s' %(self.state, self.unit, len(self), round(self.cash, 3), self.is_adj)
        return x
        
    
    @property
    def cash(self):
        return self._cash
    @cash.setter
    def cash(self, v):
        self._cash = v
        
    @property
    def state(self):
        return self._state
    @state.setter
    def state(self, v):
        if v in ['settle', 'order', 'trade']:
            self._state = v
        else:
            raise ValueError('Unlegal state value')
            
    @property
    def unit(self):
        return self._unit
    @unit.setter
    def unit(self, v):
        if v in ['cash', 'share']:
            self._unit = v
        else:
            raise ValueError('Unlegal unit value')

    @property
    def is_adj(self):
        return self._is_adj
    @is_adj.setter
    def is_adj(self, v):
        if isinstance(v, bool):
            self._is_adj = v
        else:
            raise ValueError('Unlegal is_adj value')
            
    def recover(self):
        if self.unit == 'share':
            x = (self * self.__select__(self._adj_key)) if self.is_adj else (self / self.__select__(self._adj_key)) 
        else:
            x = self.copy()
        x.is_adj = False if self.is_adj else True
        return x
    
    @property
    def day(self):
        return self.name
    @day.setter
    def day(self, v):
        if not self.is_adj and self.unit == 'share' and self.name != pd.to_datetime(v):
            post_factor = self.__select__(self._adj_key)
            self.name =  pd.to_datetime(v)
            self = self * self.__select__(self._adj_key) / post_factor
        else:
            self.name =  pd.to_datetime(v)
        
    def day_shift(self, count=1):
        x = self.copy()
        x.day = x.data_source.__shift__(x.day, count)
        return x
    
    @property
    def settle(self):
        def price(price_key=None):
            price_key = 'S_DQ_' + ('ADJ' if self._is_adj else '') + self._settle_price if price_key is None else price_key
            return self.__select__(price_key)
        
        def assets(rebalance_assets=None):
            if self.unit == 'cash' and rebalance_assets is None:
                return self.copy()
            elif self.unit == 'cash' and self.cash == 0 and rebalance_assets is not None:
                return self / [self.sum(min_count=1)] * rebalance_assets
            elif self.unit == 'cash' and self.cash != 0 and rebalance_assets is not None:
                raise ValueError('can not rebalance for cash not equal 0')
            else:
                x = self * price()
                x.unit = 'cash'
                return x
                
        def tot_assets():
            return assets().sum() + self.cash
        
        def share():
            if self.unit == 'share':
                return self.copy()
            else:
                x = self / price()
                x.unit = 'share'
                return x
        def diff_rebalance():
            x = self.copy()
            x.cash = assets().sum() * -1
            return x
        
        obj = type('settle', (), {'price':price, 'assets':assets, 'tot_assets':tot_assets, 'share': share, 'diff_rebalance':diff_rebalance})
        return obj
    
    @property
    def trade(self):
        def price(price_key=None):
            price_key = 'S_DQ_' + ('ADJ' if self._is_adj else '') + self._trade_price if price_key is None else price_key
            return self.__select__(price_key)
        
        def assets(rebalance_assets=None):
            if self.unit == 'cash' and rebalance_assets is None:
                return self.copy()
            elif self.unit == 'cash' and self.cash == 0 and rebalance_assets is not None:
                return self / [self.sum(min_count=1)] * rebalance_assets
            elif self.unit == 'cash' and self.cash != 0 and rebalance_assets is not None:
                raise ValueError('can not rebalance for cash not equal 0')
            else:
                x = self * price()
                x.unit = 'cash'
                return x
                
        def tot_assets():
            x = assets().sum() + self.cash
            return x
        
        def share():
            if self.unit == 'share':
                return self.copy()
            else:
                x = self / price()
                x.unit = 'share'
                return x

        def cost():
            x = assets().abs() * self._trade_cost * -1
            x.cash = 0
            return x

        def unbuyable(as_bool=False):
            x = (self > 0) & (~self.__select__(list(self._buy_limit.keys())[0])) & self.__select__(self._trade_status)
            x = x if as_bool else self[x]
            return x
            
        def unsellable(as_bool=False):
            x = (self < 0) & (~self.__select__(list(self._sell_limit.keys())[0])) & self.__select__(self._trade_status)      
            x = x if as_bool else self[x]
            return x
        
        def unstatusable(as_bool=False):
            x = (~self.__select__(self._trade_status))
            x = x if as_bool else self[x]
            return x
        
        def limit(detail=False):
            if not detail:
                x = self[(((self > 0) & self.__select__(list(self._buy_limit.keys())[0])) | ((self < 0) & self.__select__(list(self._sell_limit.keys())[0]))) & self.__select__('S_DQ_TRADESTATUS')]
            else:
                x = self.to_frame(('theoretical', 'order'))
                x.columns.names = ['KEYS', 'VALUES']
                x[('un' + list(self._buy_limit.keys())[0].lower(), list(self._buy_limit.values())[0])] = unbuyable(True).values
                x[('un' + list(self._sell_limit.keys())[0].lower(), list(self._sell_limit.values())[0])] = unsellable(True).values
                x[('un' + self._trade_status.split('_')[-1].lower(), 'bool')] = unstatusable(True).values
                x[('effective', 'trade')] = x[('theoretical', 'order')][~x.iloc[:, 1:].any(axis=1)]
            return x
        
        def diff_rebalance(sub_cost=True):
            x = self.copy()
            x.cash = assets().sum() * -1
            if sub_cost:
                x.cash = x.cash + cost().sum()
            return x
        
        obj = type('trade', (),  {'price':price, 'assets':assets, 'tot_assets':tot_assets, 'share': share, 'cost':cost, 
                                  'unbuyable':unbuyable, 'unsellable':unsellable, 'unstatusable':unstatusable, 
                                  'limit':limit, 'diff_rebalance':diff_rebalance})
        return obj
    
    def __calcable__(self, series):
        if isinstance(series, self.__class__):
            return any([self.unit == series.unit == 'cash', (self.unit == series.unit == 'share') & (self.is_adj == series.is_adj)])
        else:
            return True
        
    def __state__(self, others):
        state = ['order', 'settle', 'trade']
        index = min([state.index(self.state), state.index(getattr(others, 'state', 'trade'))])
        return state[index]
    
    def __times__(self, others):
        return max([self.name, getattr(others, 'name', self.name)])
        
    def like(self, like_Series):
        if self.__calcable__(like_Series):
            return self
        else:
            attr = getattr(self, 'settle' if self.state in ['settle', 'order'] else 'trade')
            if self.unit != like_Series.unit:
               attr = attr.assets() if like_Series.unit == 'cash' else attr.share()
            if self.is_adj != like_Series.is_adj:
                attr = attr.recover()
            return attr
        
    def __add__(self, others):
        if self.__calcable__(others):
            x = super().__add__(others)
            x.state = self.__state__(others)
            x.cash = x.cash + getattr(others, 'cash', 0)
            self.__times__(others)
            x.name = self.__times__(others)
            return x
        else:
            raise ValueError('__add__')
        
    def add(self, others, fill_value=0):
        if self.__calcable__(others):
            x = super().add(others, fill_value=fill_value)
            x.state = self.__state__(others)
            x.cash = x.cash + getattr(others, 'cash', 0)
            x.name = self.__times__(others)
            return x
        else:
            raise ValueError('add')
        
    def __sub__(self, others):
        if self.__calcable__(others):
            x = super().__sub__(others)
            x.state = self.__state__(others)
            x.cash = x.cash - getattr(others, 'cash', 0)
            x.name = max([self.name, getattr(others, 'name', self.name)]) 
            x.name = self.__times__(others)
            return x
        else:
            raise ValueError('__sub__')
            
    def sub(self, others, fill_value=0):
        if self.__calcable__(others):
            x = super().sub(others, fill_value=fill_value)
            x.state = self.__state__(others)
            x.cash = x.cash + getattr(others, 'cash', 0)
            x.name = self.__times__(others)
            return x
        else:
            raise ValueError('sub')
                            
    def __mul__(self, others):
        if isinstance(others, (int, float, np.number)):
            x = super(Series, self).__mul__(others)
            x.cash = x.cash * others
        else:
            x = super().__mul__(others)
        x.name = self.name
        x.state = self.state
        return x
    
    def __truediv__(self, others):
        if isinstance(others, (int, float, np.number)):
            x = super(Series, self).__truediv__(others)
            x.cash = x.cash / others
        else:
            x = super().__truediv__(others)
        x.state = self.state
        x.name = self.name
        return x

    def astate(self, state, sub_cost=False):
        if self.state in ['order', 'settle']:
            if state in ['order', 'settle']:
                x = self.copy()
                x.state = state
            else:  # state == 'trade
                x = self.copy().day_shift(1).trade.limit(False).trade.diff_rebalance(sub_cost)
                x.state = 'trade'
        else: # state == 'trade
            x = self.copy()
            x.state = state
        return x
    
    def aunit(self, unit):
        x = getattr(getattr(self, self.state if self.state == 'trade' else 'settle'), unit if unit == 'share' else 'assets')()
        return x
            
class link():
    def __init__(self, order, hold=None, init_cash=10000000, standard=True):
        self._standard = standard
        if hold is None:
            self._hold = Series(name=order.name, cash=init_cash, state='settle', unit='share')
        elif isinstance(hold, Series):
            if hold.day != order.day:
                x = hold.copy()
                x.day = order.day
                self._hold = x
            else:
                self._hold = hold
        elif isinstance(hold, self.__class__):
            x = hold.done
            if x.day != order.day:
                x.day = order.day
            self._hold = x
        self._order = order.settle.assets(self._hold.settle.tot_assets()).settle.share()
            
    @property
    def hold(self):
        if self.standard and self._hold.is_adj:
            return self._hold.recover()
        else:
            return self._hold
    
    @property
    def order(self):
        if self.standard and self._order.is_adj:
            x = self._order.recover()
        else:
            x = self._order
        return x
    
    @property
    def standard(self):
        return self._standard
    @standard.setter
    def standard(self, v):
        self._standard = v
    
    @property
    def trade(self):
        order_obj = self.order.like(self.hold).sub(self.hold)
        trade_obj = order_obj.astate('trade', False)
        if self.standard:
            trade_obj = trade_obj.round(-2) 
            trade_obj[((trade_obj + self.hold).abs() < 100) & (trade_obj < 0)] = order_obj
        return trade_obj
        
    @property
    def done(self):
        x = self.hold.add(self.trade.trade.diff_rebalance(True))
        x = x[x != 0].dropna()
        return x
    
    @property
    def trade_different(self):
        obj = self.order.sub(self.hold)
        x = obj.day_shift(1).trade.limit(True)
        if self.standard:
            x.iloc[:, -1] = x.iloc[:, -1].round(-2).fillna(0)
        x[('theoretical','price')] = obj.settle.price()
        x[('theoretical', 'payment')] = obj.settle.assets() * -1 
        x[('effective', 'price')] = self.trade.trade.price()
        x[('effective', 'payment')] = self.trade.trade.assets() * -1 
        x[('cost', 'payment')] = self.trade.trade.cost()
        x[('effective', 'different')] = x[('effective', 'payment')].fillna(0) - x[('theoretical', 'payment')] + x[('cost', 'payment')].fillna(0)
        x = x[(x.iloc[:, 0].notnull()) & (x.iloc[:, 0] != 0)]
        return x

    @property
    def returns(self):
        return self.done.settle.tot_assets() / self.hold.settle.tot_assets() - 1
    
    @property
    def turnover(self):
        return self.trade.trade.assets().abs().sum() / self.hold.settle.tot_assets()
    
    @property
    def assets(self):
        return self.done.settle.tot_assets()
    
    def __call__(self, order_Series, standard=None):
        standard = self.standard if standard is None else standard
        return self.__class__(order_Series, self.done, standard=standard)
    
    def __repr__(self):
        hold = round(self._hold.settle.tot_assets(), 4)
        theoretical = round(self.order.day_shift().settle.tot_assets(), 4)
        effective = round(self.done.settle.tot_assets(), 4)
        str_obj = 'hold  time: %s, portfolio assets: %s\ntrade time: %s, portfolio assets: %s\nturnover: %s,                trade cost: %s\ntheoretical returns: %s,    effective returns: %s' %(self.hold.day, hold, self.trade.day, round(self.done.settle.tot_assets(), 4), round(self.turnover, 4), round(self.trade.trade.cost().sum(), 4), round(theoretical / hold - 1, 4), round(effective / hold - 1, 4))
        return str_obj        
   
    
class chain():
    def __init__(self, _DataFrame, init_cash=100000000, standard=False, show=True):
        self.data = _DataFrame
        self.init_cash = init_cash
        self.standard = standard
        self.show = show
        
    def __call__(self):
        if self.show:
            begin = pd.Timestamp.today()
            print(begin)
        days = list(Series.data_source.internal_data.values())[0].index
        df_obj = self.data.loc[days[0]: days[-1]]
        dic = {}
        hold = link(df_obj.iloc[0].dropna().settle.assets(self.init_cash).settle.share(), None, self.init_cash, self.standard)
        dic[hold.hold.name] = hold
        count = 0
        for i, j in df_obj.iloc[1:-1].iterrows():
            try:
                hold = hold(j.dropna(), standard=self.standard)
                dic[hold.hold.name] = hold
                if days[days.get_loc(i) + 1].month != j.name.month or i == df_obj.index[-2]:
                    if self.show:
                        print(i, round(hold.hold.settle.tot_assets(), 2))
            except:
                print('error %s' %(i))
                count += 1
            if count > 2:
                break
        if self.show:
            print(pd.Timestamp.today() - begin)
        self.dic_obj = dic
        self.check_at = list(dic.keys())[0]
        
    @property    
    def assets(self):
        dic = self.dic_obj
        x = {i:j.hold.settle.tot_assets() for i,j in dic.items()}
        last = list(dic.values())[-1].done
        x[last.name] = last.settle.tot_assets()
        x = pd.Series(x)
        return x
   
    @property
    def returns(self):
        dic = self.dic_obj
        x = {i:(j.hold.settle.tot_assets(), j.order.day_shift().settle.tot_assets()) for i,j in dic.items()}
        last = list(dic.values())[-1].done
        x[last.name] = (last.settle.tot_assets(), np.nan)
        x = pd.DataFrame(x).T
        x = [x.iloc[:, 0].pct_change(), (x.iloc[:, 1] / x.iloc[:, 0]).shift() - 1]
        x = pd.concat(x, axis=1)
        x.index.name = 'TRADE_DT'
        x.columns = pd.MultiIndex.from_product([['effective', 'theoretical'], ['returns']])
        return x
    
    @property
    def turnover(self):
        dic = self.dic_obj
        x = {i:j.turnover for i,j in dic.items()}
        last = list(dic.values())[-1].done
        x[last.name] = np.nan
        x = pd.Series(x).shift()
        return x
    
    def get(self, date=None):
        date = self.check_at if date is None else date
        x = pd.to_datetime(pd.to_datetime(date).date()) + pd.Timedelta(15, 'h')
        self.check_at = x
        return self.dic_obj[x]
    
    @property
    def days(self):
        return pd.DatetimeIndex(self.dic_obj.keys())
    
    def shift(self, n=1):
        x = self.days
        self.check_at = x[x.get_loc(self.check_at) + n]
        
    



















