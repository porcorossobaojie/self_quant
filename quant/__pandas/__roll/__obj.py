# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 15:32:52 2022

@author: Porco Rosso
"""

import numpy as np
import pandas as pd
from __pandas.__roll.base import ts_argsort_unit, ts_rank_unit, ts_sort_unit
from __pandas.__roll.config import __obj as config

class _meta():
    def __init__(self, df_obj, window, min_periods, ts_func, ascending):
        self._obj = df_obj
        self.window = window
        self.min_periods = min_periods
        self._ts_func = ts_func
        self._ascending = ascending
        
    def __call__(self, count=None):
        if count is not None:
            self._count = count
        return self
    
    @property    
    def count(self):
        x = getattr(self, '_count', self.window)
        return x
    
    @property
    def _masked_obj(self):
        if not hasattr(self, '_masked_obj_'):
            obj = self._obj.values
            self._masked_obj_ = np.ma.array(obj, mask=np.isnan(obj))
        return self._masked_obj_
    
    @property
    def _min_periods_mask(self):
        if not hasattr(self, '_min_periods_mask_'):   
            obj = self._obj.notnull().rolling(self.window, min_periods=self.window).sum()
            self._min_periods_mask_ = obj
        return self._min_periods_mask_
    
    def _rolling_obj(self, array_obj, pct, group_func, **kwargs):
        idx_0, idx_1 = array_obj.shape
        outer = []
        window = self.window
        ascending = self._ascending
        count = self.count * (1 if ascending else -1)
        for i in range(window, idx_0 + 1):
            obj = array_obj[i - window: i]
            obj = self._ts_func(obj, cut=count, pct=pct, func=group_func, **kwargs)
            outer.append(obj)
        df = np.ma.concatenate(outer).reshape(-1, idx_1)
        lens = int(df.shape[0] / (idx_0 - window + 1))
        index = pd.MultiIndex.from_product([self._obj.index[window - 1:], range(lens)], names=[self._obj.index.name, 'RANGE']) if lens > 1 else self._obj.index[window - 1:]
        df = pd.DataFrame(df, index=index, columns=self._obj.columns)
        return df
    
    def _apply(self, array_obj, group_func, **kwargs):
        return self._rolling_obj(array_obj, pct=None, group_func=group_func, **kwargs)
    
class _max(_meta):
    
    def __init__(self, df_obj, window, min_periods):
        super().__init__(df_obj, window, min_periods, ts_sort_unit, False)
    
    def mean(self):
        x = self._rolling_obj(self._masked_obj, False, np.nanmean)
        x = x.reindex(self._obj.index)
        x = x[self._min_periods_mask >= self.min_periods]
        return x
        
    def std(self):
        x = self._rolling_obj(self._masked_obj, False, np.nanstd)
        x = x.reindex(self._obj.index)
        x = x[self._min_periods_mask >= self.min_periods]
        return x
    
    def sum(self):
        x = self._rolling_obj(self._masked_obj, False, np.nansum)
        x = x.reindex(self._obj.index)
        x = x[self._min_periods_mask >= self.min_periods]
        return x
    
    def apply(self, function, **func_kwds):
        x = self._apply(self._masked_obj, function, **func_kwds)
        x = x.reindex(self._obj.index)
        x = x[self._min_periods_mask >= self.min_periods]
        return x
    
    @property
    def values(self):
        x = self._rolling_obj(self._masked_obj, False, None)
        return x

class _min(_max, _meta):
    
    def __init__(self, df_obj, window, min_periods):
        _meta.__init__(self, df_obj, window, min_periods, ts_sort_unit, True)

class _rank(_meta):
    
    def __init__(self, df_obj, window, min_periods):
        super().__init__(df_obj, window, min_periods, ts_rank_unit, False)

    def __call__(self, pct):
        x = self._rolling_obj(self._obj.values, pct, None)
        x = x.reindex(self._obj.index)
        x = x[self._min_periods_mask >= self.min_periods]
        return x
    
class _rolls():
    def __init__(self, pandas_obj, window, min_periods=None):
        self._obj = pandas_obj
        self.window = window
        self.min_periods = min_periods if min_periods is not None else window
        self._max_class = _max(pandas_obj, self.window, self.min_periods)
        self._min_class = _min(pandas_obj, self.window, self.min_periods)
        self._rank_class = _rank(pandas_obj, self.window, self.min_periods)
        
    def max(self, count=None):
        count = self.window if count is None else count
        x = self._max_class(count)
        return x
    
    def min(self, count=None):
        count = self.window if count is None else count
        x = self._min_class(count)
        return x
        
    def ts_rank(self, pct=True):
        x = self._rank_class(pct)
        return x
    
@pd.api.extensions.register_series_accessor(config.pandasAttrName)
class rolls():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        
    def __call__(self, window, min_periods=None):
        x = _rolls(self._obj.to_frame(), window, min_periods)
        return x
    
@pd.api.extensions.register_dataframe_accessor(config.pandasAttrName)
class rolls():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        
    def __call__(self, window, min_periods=None):
        x = _rolls(self._obj, window, min_periods)
        return x
    
    
    
    

