# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 14:23:57 2021

@author: Porco Rosso
"""

import pandas as pd
from flow.__tables.base import __get__, __finance_shift__, __finance_quarter_adjust__

class meta():
    
    def __init__(self, **kwargs):
        pass
    
    @classmethod
    def __shift__(cls, df, n):
        x = __finance_shift__(df, n) if isinstance(df, pd.DataFrame) else df
        return x
    
    @classmethod
    def __Q_adj__(cls, df):
        x = __finance_quarter_adjust__(df) if isinstance(df, pd.DataFrame) else df
        return x
            
    def get(self, keys, name=None, end=None, **kwargs):
        x = __get__(obj         = self, 
                    attr        = 'values', 
                    schemas     = self.schemas, 
                    table       = self.table, 
                    index_key   = self.index, 
                    columns_key = self.columns, 
                    value_keys  = keys, 
                    filter_key  = self.filter_key, 
                    filter_min  = self.filter_min,
                    filter_max  = self.filter_max,
                    where       = self.where, 
                    name        = name,
                    **kwargs) 
        if isinstance(x, pd.DataFrame):
            if len(x.index.names) > 1:
                x = x[x.index.get_level_values(self.filter_key) <= end] if end is not None else x
                x.index = x.index.droplevel(self.filter_key)
                x = x.iloc[:, 0] if isinstance(keys, str) else x
                x = x.unstack(-1).sort_index().sort_index(axis=1)
                end = pd.Timestamp.today() if end is None else end
                x = x.reindex(pd.date_range(x.index[0], end, freq='Q'))
            else:
                x.columns = x.columns.get_level_values(-1) if isinstance(keys, str) else x.columns
        else:
            x.index = x.index.get_level_values(-1) if isinstance(keys, str) else x.index
        return x
    
    def __call__(self, keys, name=None, end=None, quarter=False, shift=None):
        name = pd.to_datetime(name) if isinstance(name, str) else name
        end = pd.to_datetime(end) if end is not None else end
        x = self.get(keys, name, end)
        x = self.__class__.__Q_adj__(x) if quarter else x
        x = self.__class__.__shift__(x, shift) if shift is not None else x
        return x
    

        
        
                
    








