# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 11:20:28 2024

@author: Porco Rosso
"""

from __data__.future.ic import config

import flow
import pandas as pd
import __pandas

DATA_SOURCE = {i.split('.')[0]: pd.read_csv(config.PATH + '/' + i).set_index('date') for i in config.FILES}
DATA_SOURCE = pd.concat(DATA_SOURCE, axis=1)


class time_cut():
    data_source = DATA_SOURCE
    def __init__(self, time, slice_series=True):
        self.time = time
        if slice_series:
            self._data = self.data_source.loc[self.time]
    
    @property
    def time(self):
        return self._time
    @time.setter
    def time(self, v):
        self._time = pd.to_datetime(v)
        
    @property
    def data(self):
        if not hasattr(self, '_data'):
            return self.data_source.loc[self.time]
        else:
            return self._data
            
class future_cut():
    data_source = DATA_SOURCE
    def __init__(self, future, slice_series=True):
        self.future = future
        if slice_series:
            self._data = self.data_source[self.future]
            
    @property
    def future(self):
        return self._future
    @future.setter
    def future(self, v):
        if isinstance(v, str):
            v = [v]
        obj = []
        for i in v:
            obj = obj + self.data_source.columns.get_level_values(0)[self.data_source.columns.get_level_values(0).str.contains(i)].to_list()
        obj = sorted(list(set(obj)))
        if len(obj) == 1:
            obj = obj[0]
        self._future = obj
        
    @property
    def data(self):
        if not hasattr(self, '_data'):
            return self.data_source[self.future]
        else:
            return self._data
        
        
class holding():
    def __init__(self, future_df):
        self._data = future_df.dropna(how='all')
    
    def calc(self, time=None, history=None, unit_price=200):
        if (time is None) and (history is None):
            df = self._data.iloc[:1]
            df['price'] = df['money'] / unit_price







































