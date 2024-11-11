# -*- coding: utf-8 -*-
"""
Created on Mon Dec  6 21:25:33 2021

@author: Porco Rosso
"""

import numpy as np
import pandas as pd
import __pandas

from __capital__.functions.base import __source__, __shift__

from __capital__.data_obj.config import main as config

import flow

class main():
    def __init__(self, **kwargs):
        pass
    
    def data_init(self):
        flow.stock(config.params['ashareeodprices']).stack()    
        
    @property
    def _internal_data(self):
        if not hasattr(self, '_data_obj'):
            df = flow.stock(config.params['ashareeodprices']).stack()
            df['S_DQ_TRADESTATUS'] = df['S_DQ_TRADESTATUS'].fillna(0).astype(bool)
            alter_columns = ['S_DQ_PCTCHANGE', 'S_DQ_LOW', 'S_DQ_HIGH', 'S_DQ_OPEN', 'S_DQ_ADJAVGPRICE']
            hold = pd.DataFrame(np.repeat(df['S_DQ_TRADESTATUS'].values, 5).reshape(-1, 5), index=df.index, columns=alter_columns)
            df[alter_columns] = df[alter_columns][hold]
            df = df.unstack()
            st = flow.is_st().astype(bool).reindex(df.index).fillna(method='ffill')
            dic = {}
            dic['BUY_LIMIT'] = df['S_DQ_HIGH_LIMIT'] / df['S_DQ_LOW'] - 1
            dic['SELL_LIMIT'] = 1 - df['S_DQ_LOW_LIMIT'] / df['S_DQ_HIGH']
            dic['IS_ST'] = st
            dic['S_DQ_ADJOPEN'] = df['S_DQ_OPEN'] * df['S_DQ_POST_FACTOR']
            dic['S_DQ_PREADJCLOSE'] = df['S_DQ_ADJCLOSE'].shift()
            dic = pd.concat(dic, axis=1)
            dic.columns.names = ['KEYS', 'S_INFO_WINDCODE']
            df = pd.concat([df, dic], axis=1)
            self._data_obj = df
        return self._data_obj

    @property
    def __days__(self):
        return self._internal_data.index

    def __trade_status__(self, dates=None, columns=None, reverse=False):
        x = __source__(self._internal_data, dates, 'S_DQ_TRADESTATUS', columns)
        return ~x if reverse else x
    
    def __is_ST__(self, dates=None, columns=None):
        x = __source__(self._internal_data, dates, 'IS_ST', columns)
        return x
    
    def __buy_limit__(self, dates=None, columns=None, limit=0.005, reverse=True):
        x = __source__(self._internal_data, dates, 'BUY_LIMIT', columns)
        x = x < limit
        x = ~x if reverse else x
        return x
    
    def __sell_limit__(self, dates=None, columns=None, limit=0.005, reverse=True):
        x = __source__(self._internal_data, dates, 'SELL_LIMIT', columns)
        x = x < limit
        x = ~x if reverse else x
        return x
        
    def __source__(self, dates=None, keys=None, columns=None):
        return __source__(self._internal_data, dates, keys, columns)
    
    def __shift__(self, index_obj, date, shift):
        return __shift__(index_obj, date, shift)
    









