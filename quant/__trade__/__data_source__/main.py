# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 17:55:53 2022

@author: Porco Rosso
"""

import pandas as pd
import numpy as np
import __pandas
from __trade__.__data_source__.config import main as config

class main(config):
    def __init__(self, buy_limit={'BUYABLE':0.005}, sell_limit={'SELLABLE': 0.005}, st_info={'ST_LIMIT':2}, **kwargs):
        self._buyable = buy_limit
        self._sellable = sell_limit
        self._st_limit = st_info
        
    def __call__(self, buy_limit=None, sell_limit=None, st_info=None, **kwargs):
        buy_limit = self._buyable if buy_limit is None else buy_limit
        sell_limit = self._sellable if sell_limit is None else sell_limit
        st_info = self._st_limit if st_info is None else st_info
        if not hasattr(self, '_internal_data'):
            trade_df, st_df = [pd.SQL.read(**i) for i in self.table_info]
            trade_df = trade_df.set_index(['TRADE_DT', 'S_INFO_WINDCODE']).unstack()
            df_obj = {i:trade_df[i] for i in trade_df.columns.get_level_values(0).unique()}
            df_obj['S_DQ_TRADESTATUS'] = df_obj['S_DQ_TRADESTATUS'].fillna(0).astype(bool)
            st_obj = st_df.set_index(['TRADE_DT',  'S_INFO_WINDCODE'])['S_DQ_ST'].unstack()
            st_obj = st_obj.reindex(sorted(set(trade_df.index) | set(st_obj.index))).fillna(method='ffill').fillna(0).reindex(trade_df.index)
            df_obj['S_DQ_ST'] = st_obj
        else:
            df_obj = getattr(self, '_internal_data')
        for i, j in buy_limit.items():
            df_obj[i] = (df_obj['S_DQ_LOW'] / df_obj['S_DQ_HIGH_LIMIT'] + j) <= 1
        for i,j in sell_limit.items():
            df_obj[i] = (df_obj['S_DQ_HIGH'] / df_obj['S_DQ_LOW_LIMIT']) >= j + 1
        for i,j in st_info.items():
            df_obj[i] = df_obj['S_DQ_ST'] >= j
        self._internal_data = df_obj
        self._buyable = buy_limit
        self._sellable = sell_limit
        self._st_limit = st_info
            
            
    @property
    def internal_data(self):
        if not hasattr(self, '_internal_data'):
            self.__call__()
        return self._internal_data
        
    def __set_limit__(self, buy_limit, sell_limit, st_info):
        df_obj = self.internal_data
        if buy_limit is not None:
            self._buyable = buy_limit
            for i, j in self._buyable.items():
                df_obj[i] = (df_obj['S_DQ_LOW'] / df_obj['S_DQ_HIGH_LIMIT'] + j) <= 1
        if sell_limit is not None:
            self._sellable = sell_limit
            for i,j in self._sellable.items():
                df_obj[i] = (df_obj['S_DQ_HIGH'] / df_obj['S_DQ_LOW_LIMIT']) >= j + 1
        if st_info is not None:
            self._st_limit = st_info
            for i,j in self._st_limit.items():
                df_obj[i] = df_obj['S_DQ_ST'] >= j
        self._internal_data = df_obj
        
    def __shift__(self, date, shift):
        x = list(self.internal_data.values())[0]
        count = x.index.get_loc(date) + shift
        return x.index[count]
        
    def __select__(self,keys, trade_dt=None, columns=None):
        x = self.internal_data[keys]
        trade_dt = x.index if trade_dt is None else trade_dt
        columns = x.columns if columns is None else columns
        x = x.loc[trade_dt, columns]
        return x
    
    def __filter__(self, *series):
        trade_dt = sorted(set([i.name for i in series]))
        columns = series[0].index
        for i in series[1:]:
            columns = columns.append(i.index)
        columns = columns.drop_duplicates().sort_values()
        return  {'trade_dt':trade_dt, 'columns':columns}
        
