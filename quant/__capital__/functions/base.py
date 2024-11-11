# -*- coding: utf-8 -*-
"""
Created on Wed Jul 14 15:29:35 2021

@author: Porco Rosso
"""

import pandas as pd

def __shift__(index_obj, date, shift):
    x = index_obj.get_loc(date) + shift
    return index_obj[x]

def __source__(df, dates, keys, columns):
    x = df.loc[dates] if dates is not None else df
    x = x[keys] if keys is not None else x
    if x.index.nlevels > 1:
        keys = df.columns.get_level_values(0).unique() if keys is None else keys
        columns = pd.MultiIndex.from_product([keys, columns], names=df.columns.names)
    x = (x.reindex(columns) if x.ndim == 1 else x.reindex(columns, axis=1)) if columns is not None else x
    return x


        
        
    
    







