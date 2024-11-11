# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 11:18:08 2021

@author: Porco Rosso
"""

import pandas as pd
import __pandas

def __get_from_sql__(schemas, table, index_key, columns_key, value_keys, filter_key=None, filter_min=None, filter_max=None, where=None, **kwargs):
    filter_key = index_key if filter_key is None else filter_key
    mini = '%s >= "%s"' %(filter_key, filter_min) if filter_min is not None else None
    maxi = '%s <= "%s"' %(filter_key, filter_max) if filter_max is not None else None
    where = ' AND '.join([i for i in [mini, maxi, where] if i is not None])
    where = None if where == '' else where
    #value_keys = [value_keys] if isinstance(value_keys, str) else value_keys
    get_columns = list(set([i for i in [filter_key, index_key, columns_key, *value_keys] if i is not None]))
    x = pd.SQL.read(schemas, table, get_columns, where)
    if filter_key == index_key:
        x = x.set_index([index_key, columns_key]).unstack(columns_key)
        x.columns.names = ['VALUES', columns_key]
    else:
        x = x.set_index([filter_key, index_key, columns_key])
        x.columns.name = 'VALUES'
    try:
        x = x.astype('float64')
    except:
        pass
    return x

def __unget_from_attr__(obj, attr, value_keys, **kwargs):
    x = getattr(obj, attr).columns.get_level_values(0).unique()
    x = list(set(value_keys) - set(x))
    return x

def __get__(obj, attr, schemas, table, index_key, columns_key, value_keys, filter_key, filter_min, filter_max, where, name, **kwargs):
    value_keys = [value_keys] if isinstance(value_keys, str) else value_keys
    key_to_sql = __unget_from_attr__(obj, attr, value_keys, **kwargs)
    if len(key_to_sql):
        values = __get_from_sql__(schemas, table, index_key, columns_key, key_to_sql, filter_key, filter_min, filter_max, where, **kwargs)
        setattr(obj, attr, pd.concat([getattr(obj, attr), values], axis=1))
    x = getattr(obj, attr)[value_keys]
    x = x if name is None else (x.iloc[name] if isinstance(name, int) else x.loc[name])
    return x

def __finance_shift__(df, n):
    bools = df.iloc[-1].isnull()
    while n > 0 and bools.any():
        n -= 1
        df.loc[:, bools] = df.loc[:, bools].shift()
        bools = df.iloc[-1].isnull()
    return df

def __finance_quarter_adjust__(df):
    tmp = df[(df.index.month == 3) & (df.index.day == 31)]
    df = df.diff()
    df.loc[tmp.index] = tmp
    return df
        
    
    
    

        
    
    







