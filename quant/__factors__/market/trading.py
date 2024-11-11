# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 12:03:35 2021

@author: Porco Rosso
"""

from __factors__.base.main import main as meta
from __factors__ import barra
from __factors__.market.config import main as config

import pandas as pd
import __pandas
import numpy as np


class main(meta):

    def data_init(self):
        self.initialize(**config.params)

    @property
    def open(self):
        return self.stock('s_dq_open')
    
    @property
    def close(self):
        return self.stock('s_dq_close')
    
    @property
    def low(self):
        return self.stock('s_dq_low')
    
    @property
    def high(self):
        return self.stock('s_dq_high')
    
    @property
    def avg(self):
        return self.stock('s_dq_avgprice')
    
    @property
    def pct_change(self):
        return self.stock('s_dq_pctchange')
    
    @property
    def amount(self):
        return self.stock('s_dq_amount')
    
    @property
    def volume(self):
        return self.stock('s_dq_volume')

    @property
    def turnover(self):
        return self.stock('s_dq_freeturnover')
    
    @property
    def adj_close(self):
        return self.stock('s_dq_adjclose')
        
    @property
    def adj_avg(self):
        return self.stock('s_dq_adjavgprice')
    '''    
    # amount / free turnover / volume in Voltility
    def AMOUNT_STD(self, rolling_list=[42, 63, 126], neutral=True, neu_factors=None):
        amount = self.amount
        pct = self.pct_change
        obj = {i:amount.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def AMOUNT_STD_DIFF_1(self, rolling_list=[42, 63, 126], neutral=True, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_STD(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
        
    def AMOUNT_STD_DIFF_2(self, rolling_list=[42, 63, 126], neutral=True, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_STD_DIFF_1(rolling_list, neutral, neu_factors).diff()
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
    def AMOUNT_STD_STD_1(self, rolling_list=[42, 63, 126], neutral=True, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_STD(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
            
        return obj * -1
        
    def AMOUNT_STD_STD_2(self, rolling_list=[42, 63, 126], neutral=True, neu_factors=None):
        pct = self.pct_change
        obj = self.AMOUNT_STD_STD_1(rolling_list, neutral, neu_factors)
        obj = {i:obj.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        obj = pd.concat(obj, axis=1).stack().mean(axis=1).unstack().stats.standard(axis=1)
        obj = obj.stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid
        if neutral:
            obj = barra.barra_neutral(obj, neu_factors)
        return obj * -1
    
        '''

    def TURNOVER_Z(self, rolling_list=[10, 15, 20, 25, 30, 35, 40, 45]):
        turn = self.turnover
        obj = {i:turn.rolling(i) for i in rolling_list}
        obj = {i: j.mean() / j.std() for i,j in obj.items()}
        x = pd.concat(obj, axis=1).stack().sum(min_count=len(rolling_list), axis=1) / len(rolling_list)
        x = x.unstack()
        x = x.stats.standard(axis=1)
        return x
    
    def TURNOER_STD(self, rolling_list=[21, 42, 63, 126]):
        pct = self.pct_change
        turn = self.turnover
        obj = {i:turn.rolling(i).std() for i in rolling_list}
        x = pd.concat(obj, axis=1).stack()
        x = x.div(x.iloc[:, -1], axis=0).replace(0, np.nan).iloc[:, :-1].sum(axis=1, min_count=1)
        x = x.unstack().stats.neutral(neu_axis=1, pct=pct.rolling(3).mean()).resid.stats.standard(axis=1)
        return x
    
    def AMOUNT_Z(self, rolling_list=[10, 15, 20, 25, 30, 35, 40, 45]):
        dic = {}
        turn = {'volume': self.volume, 'amount':self.amount, 'turnover':self.turnover}
        for key, value in turn.items():
            obj = {i:value.rolling(i) for i in rolling_list}
            obj = {i: j.mean() / j.std() for i,j in obj.items()}
            x = pd.concat(obj, axis=1).stack().sum(min_count=len(rolling_list), axis=1) / (len(rolling_list))
            x = x.unstack()
            dic[key] = x
        dic = pd.concat(dic, axis=1).stack().sum(min_count=3, axis=1)
        x = dic.unstack().stats.standard(axis=1)
        return x
    
    def AMOUNT_STD(self, rolling_list=[10, 15, 20, 25, 30, 35, 40, 45]):
        dic = {}
        turn = {'volume': self.volume, 'amount':self.amount, 'turnover':self.turnover}
        for key, value in turn.items():
            obj = {i:value.rolling(i) for i in rolling_list}
            obj = {i: j.std() for i,j in obj.items()}
            x = pd.concat(obj, axis=1).stack().sum(min_count=len(rolling_list), axis=1) / (len(rolling_list))
            x = x.unstack()
            dic[key] = x
        dic = pd.concat(dic, axis=1).stack().sum(min_count=3, axis=1)
        x = dic.unstack().stats.standard(axis=1)
        return x
    
    def AMOUNT_TS(self, rolling_list=[20, 25, 30, 35]):
        dic = {}
        turn = {'volume': self.volume, 'amount':self.amount, 'turnover':self.turnover}
        for key, value in turn.items():
            obj = {i:value.rollings(i).ts_rank() for i in rolling_list}
            x = pd.concat(obj, axis=1).stack().sum(min_count=len(rolling_list), axis=1) / (len(rolling_list))
            x = x.unstack()
            dic[key] = x
        dic = pd.concat(dic, axis=1).stack().sum(min_count=3, axis=1)
        x = dic.unstack().stats.standard(axis=1)
        return x
    
    
    
    def DEVIATION_CORR_TURNOVER(self, rolling_list=[5, 10, 15, 20]):
        high = self.high
        low = self.low
        close = self.close
        turn = self.turnover
        pct = (high - low) / close
        obj = {i:pct.rolling(i, min_periods=rolling_list[0]).corr(turn) for i in rolling_list}
        obj = {i: j[(j >= -1) & (j <= 1)] for i,j in obj.items()}
        x = pd.concat(obj, axis=1).stack().sum(min_count=len(rolling_list), axis=1) / len(rolling_list)
        x = x.unstack()
        x = x.stats.standard(axis=1)
        return x
    
    def OPEN_ABNORMAL(self, rolling_list=[5,6,7,8,9,10]):
        open = self.open
        close = self.close
        pct = (open / close).rank(axis=1, pct=True)
        obj = {i:pct.rolling(i, min_periods=rolling_list[0]).std() for i in rolling_list}
        x = pd.concat(obj, axis=1).stack().sum(min_count=len(rolling_list), axis=1) / len(rolling_list)
        x = x.unstack()
        x = x.stats.standard(axis=1)
        return x
    
    def VOLUME_HIGH(self, rolling_list=[5, 10, 15, 20]):
        high = self.high
        amount = self.amount
        x = {i:high.rollings(i).ts_rank().rolling(i).corr(amount.rollings(i).ts_rank()) for i in rolling_list}
        x = pd.concat(x, axis=1).stack()
        x = x[(x >= -1) & (x <= 1)]
        x = (x.sum(min_count=len(rolling_list), axis=1) / len(rolling_list)).unstack()
        x = x.stats.standard(axis=1)
        return x
    
    def VOLUME_AVG(self, rolling_list=[5, 10, 15, 20]):
        avg = self.adj_avg.rank(axis=1, pct=True)
        amount = self.amount.rank(axis=1, pct=True)
        x = {i:avg.rolling(i).corr(amount) for i in rolling_list}
        x = pd.concat(x, axis=1).stack()
        x = x[(x >= -1) & (x <= 1)]
        x = (x.sum(min_count=len(rolling_list), axis=1) / len(rolling_list)).unstack()
        x = x.stats.standard(axis=1)
        return x

    def DAY_STD(self, rolling_list=[5, 10, 15, 20]):
        low = self.low
        high = self.high
        close = self.close
        x = (high - low) / close
        x = pd.concat({i:x.rolling(i).std() for i in rolling_list}, axis=1)
        x = x.stack().sum(min_count=len(rolling_list), axis=1).unstack()
        x = x.stats.standard(axis=1)
        return x
    
    def RETURNS_CORR_TURNOVER(self, rolling_list=[5, 6, 7, 8, 9]):
        pct = self.pct_change
        turn = self.turnover.pct_change()
        obj = {i:pct.rolling(i, min_periods=rolling_list[0]).corr(turn) for i in rolling_list}
        obj = {i: j[(j >= -1) & (j <= 1)] for i,j in obj.items()}
        x = pd.concat(obj, axis=1).stack().sum(min_count=len(rolling_list), axis=1) / len(rolling_list)
        x = x.unstack().stats.neutral(neu_axis=1, re=pct.rolling(3).mean()).resid.stats.standard(axis=1)
        return x        
        
    def RETURN_MOMENTUM(self, rolling_list=[42, 63, 84]):
        # only need to neutral with me, bm, non, earning
        pct = self.pct_change
        x = pd.concat({i:pct.rolling(i).mean().shift(3) for i in rolling_list}, axis=1)
        x = x.stack().mean(axis=1).unstack().stats.neutral(neu_axis=1, re=pct.rolling(3).mean()).resid    
        x = x.stats.standard(axis=1)
        return x

    def PRICE_ABNORMAL(self, rolling_list=[5, 10, 15, 20]):
        # no need neutral
        prices = {'high': self.high, 'low': self.low, 'avg': self.avg, 'open': self.open, 'close': self.close}
        x = pd.concat(prices, axis=1)   
        x = {i:x.rolling(i).std() for i in rolling_list}
        x = pd.concat(x, axis=1).stack()
        x = x.mean(axis=1).unstack()
        x = x.stats.standard(axis=1)
        return x
        
        
